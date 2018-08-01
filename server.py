#!/usr/bin/env python
from flask import Flask, request, redirect, render_template, flash
import urllib, os, time, json

conndir = 'json/conn.json'
usrdir = 'json/user.json'

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def readfile(file):
    with open(file) as json_data_file:
        temp = json.load(json_data_file)
        json_data_file.close()
    return temp

def writefile(file,data):
    temp = open(file, "w")
    temp.write(json.dumps(data, indent=4, sort_keys=True))
    temp.close()

def login_user(ip,usr):
    conn = readfile(conndir)
    i = str(conn['connCount'] + 1)
    conn[i]['isConnect'] = 1
    conn[i]['IP'] = ip
    conn[i]['timeStart'] = time.time()
    conn[i]['usr']=usr
    conn['connCount'] = conn['connCount'] + 1
    os.system("sudo iptables -I internet " + i + " -t mangle -s " + ip + " -j RETURN")
    writefile(conndir,conn)

def logout_user(ip):
    conn = readfile(conndir)
    isFound = 0
    i = 0
    while (isFound == 0) and (i < 4) :
        i = i + 1
        j = str(i)
        if (request.remote_addr == conn[j]['IP']):
            if (i<4):
                for x in range(i,4):
                    conn[str(x)]['isConnect'] = conn[str(x+1)]['isConnect']
                    conn[str(x)]['IP'] = conn[str(x+1)]['IP']
                    conn[str(x)]['timeStart'] = conn[str(x+1)]['timeStart']
                    conn[str(x)]['usr'] = conn[str(x+1)]['usr']
            conn['4']['isConnect'] = 0
            conn['4']['IP'] = ''
            conn['4']['timeStart'] = 0
            conn['4']['usr']= ''
            os.system("sudo iptables -D internet " + j + " -t mangle")
            conn['connCount'] = conn['connCount'] - 1
            isFound = 1
    writefile(conndir,conn)

def elapsed(start):
    temp = (time.time() - start)
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    timeS = '%dh %dm %ds' %(hours,minutes,seconds)
    return timeS

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
    conn = readfile(conndir)
    isFound = 0
    i = 0
    while (isFound == 0) and (i < conn['connCount']) :
        i = i + 1
        j = str(i)
        if (request.remote_addr == conn[j]['IP']):
            isFound = 1
    if ((isFound) and  conn[j]['isConnect'] and (conn[j]['IP'] == request.remote_addr)):
        usrname = conn[j]['usr']
        ip = request.remote_addr
        timeS = elapsed(conn[j]['timeStart'])
        return render_template('success.html',ip=ip,timeS=timeS,usrname=usrname)
    else:
        if conn['connCount'] < 4:
            if request.method == 'POST' and 'login' in request.form and 'password' in request.form:
                usr = readfile(usrdir)
                isFound = 0
                i = 0
                while (isFound == 0) and (i < usr['usrCount']) :
                    i = i + 1
                    if request.form['login'] == usr[str(i)]['username'] and request.form['password'] == usr[str(i)]['password']:
                        isFound = 1
                if (isFound):
                    login_user(request.remote_addr,request.form['login'])
                    flash('Login Successful')
                else:
                    flash('Account Invalid')
                return redirect('/')
            return render_template('login.html')
        else:
            return render_template('exceeded.html')

if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
