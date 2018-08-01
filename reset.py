#!/usr/bin/env python
import json, subprocess, time

#reset Conn.json file
def rewriteConn():
    with open('json/conn.json') as json_data_file:
        conn = json.load(json_data_file)
        json_data_file.close()
    for i in range(1,5):
        k = str(i)
        conn[k]['IP']=''
        conn[k]['MAC']=''
        conn[k]['isConnect']=0
        conn[k]['timeStart']=0
        conn[k]['usr']=''
    conn['connCount'] = 0
    connect = open('json/conn.json', "w")
    connect.write(json.dumps(conn, indent=4, sort_keys=True))
    connect.close()

#clean firewall
def cleanFirewall():
    subprocess.call(["sudo /sbin/iptables -F"], shell=True)
    subprocess.call(["sudo /sbin/iptables -X"], shell=True)
    subprocess.call(["sudo /sbin/iptables -t nat -F"], shell=True)
    subprocess.call(["sudo /sbin/iptables -t nat -X"], shell=True)
    subprocess.call(["sudo /sbin/iptables -t mangle -F"], shell=True)
    subprocess.call(["sudo /sbin/iptables -t mangle -X"], shell=True)

#Configure Firewall
def initFirewall():
    subprocess.call(["sudo /sbin/iptables -N internet -t mangle"], shell=True)
    subprocess.call(["sudo /sbin/iptables -t mangle -A PREROUTING -j internet"], shell=True)
    subprocess.call(["sudo /sbin/iptables -t mangle -A internet -j MARK --set-mark 99"], shell=True)
    subprocess.call(["sudo /sbin/iptables -t nat -A PREROUTING -m mark --mark 99 -p tcp --dport 80 -j DNAT --to-destination 192.168.5.1"], shell=True)
    subprocess.call(['sudo echo "1" > /proc/sys/net/ipv4/ip_forward'], shell=True)
    subprocess.call(["sudo /sbin/iptables -A FORWARD -i eth0 -o wlan0 -m state --state ESTABLISHED,RELATED -j ACCEPT"], shell=True)
    subprocess.call(["sudo /sbin/iptables -A FORWARD -m mark --mark 99 -j REJECT"], shell=True)
    subprocess.call(["sudo /sbin/iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT"], shell=True)
    subprocess.call(["sudo /sbin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"], shell=True)

def main():
    rewriteConn()
    #cleanFirewall()
    #initFirewall()

main()
