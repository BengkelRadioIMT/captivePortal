#!/usr/bin/env python
from passlib.context import CryptContext
import json

usrdir = 'json/user.json'

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=3000
)

def readfile(file):
    with open(file) as json_data_file:
        temp = json.load(json_data_file)
        json_data_file.close()
    return temp

def writefile(file,data):
    temp = open(file, "w")
    temp.write(json.dumps(data, indent=4, sort_keys=True))
    temp.close()

def encrypt(password):
    return pwd_context.encrypt(password)

def main():
    usr = readfile(usrdir)
    for i in range(1,usr['usrCount']+1):
        tmp = usr[str(i)]['password']
        usr[str(i)]['password'] = encrypt(tmp)
    writefile('usrdir',usr)
main()
