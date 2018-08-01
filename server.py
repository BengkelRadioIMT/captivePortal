#!/usr/bin/env python

from flask import Flask, request, redirect, render_template, flash
import urllib, os, time, json

rule_count = 0

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def login_user(ip):
    with open('conn.json') as json_data_file:
        conn = json.load(json_data_file)
        json_data_file.close()
    k = str(conn['connCount'] + 1)
    conn[k]['isConnect'] = 1
    conn[k]['IP'] = ip
    conn[k]['timeStart'] = time.time()
    conn['connCount'] = conn['connCount'] + 1

    os.system("sudo iptables -I internet " + k + " -t mangle -s " + ip + " -j RETURN")

    connect = open('conn.json', "w")
    connect.write(json.dumps(conn, indent=4, sort_keys=True))
    connect.close()

def logout_user(ip):
    with open('conn.json') as json_data_file:
        conn = json.load(json_data_file)
        json_data_file.close()
    isFound = 0
    i = 0
    while (isFound == 0) and (i < 4) :
        i = i + 1
        j = str(i)
        if (request.remote_addr == conn[j]['IP']):
            if (i<4):
                for x in range(i,4):
                    y = str(x)
                    z = str(x+1)
                    conn[y]['isConnect'] = conn[z]['isConnect']
                    conn[y]['IP'] = conn[z]['IP']
                    conn[y]['timeStart'] = conn[z]['timeStart']
            conn['4']['isConnect'] = 0
            conn['4']['IP'] = ''
            conn['4']['timeStart'] = 0
            os.system("sudo iptables -D internet " + j + " -t mangle")
            conn['connCount'] = conn['connCount'] - 1
            isFound = 1
    connect = open('conn.json', "w")
    connect.write(json.dumps(conn, indent=4, sort_keys=True))
    connect.close()

@app.route('/logout')
def logout():
    ip = request.remote_addr
    logout_user(ip)
    return redirect("/")

@app.route('/favicon.png')
def favicon():
    return app.send_static_file('favicon.png')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    with open('conn.json') as json_data_file:
        conn = json.load(json_data_file)
        json_data_file.close()
    isFound = 0
    i = 0
    while (isFound == 0) and (i < conn['connCount']) :
        i = i + 1
        j = str(i)
        if (request.remote_addr == conn[j]['IP']):
            isFound = 1
    if ((isFound) and  conn[j]['isConnect'] and (conn[j]['IP'] == request.remote_addr)):
        ip = request.remote_addr
        temp = (time.time() - conn[j]['timeStart'])
        hours = temp//3600
        temp = temp - 3600*hours
        minutes = temp//60
        seconds = temp - 60*minutes
        timeS = '%dh %dm %ds' %(hours,minutes,seconds)
        return render_template('success.html',ip=ip,timeS=timeS)
    else:
        if request.method == 'POST' and 'login' in request.form and 'password' in request.form:
            if (request.form['login']=='admin') and (request.form['password']=='bengkrad181'):
                login_user(request.remote_addr)
                flash('Login Successful')
            else:
                flash('Account Invalid')
            return redirect('/')
        return render_template('login.html')

if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
