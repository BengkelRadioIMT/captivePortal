#!/usr/bin/env python

from flask import Flask, request, redirect, render_template, flash
import urllib, os, time

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def login_user(ip):
    os.system("sudo iptables -I internet 1 -t mangle -s " + ip + " -j RETURN")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'login' in request.form and 'password' in request.form:
        if (request.form['login']=='admin') and (request.form['password']=='admin'):
            login_user(request.remote_addr)
            flash('Login Successful')
            time.sleep(1)
            return redirect('https://www.google.co.id')
        else:
             flash('Account Invalid')
             return redirect("/")
    else:
        return render_template('login.html', orig_url=urllib.urlencode({'orig_url': request.args.get('orig_url', '')}))

@app.route('/favicon.png')
def favicon():
    return app.send_static_file('favicon.png')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect("http://192.168.5.1/login?" + urllib.urlencode({'orig_url': request.url}))

if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
