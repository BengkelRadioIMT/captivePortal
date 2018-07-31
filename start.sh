#!/bin/bash
# New startup call

cd /home/pi/captivePortal
<<<<<<< HEAD
sudo python reset.py
=======

#Remove old firewall
sudo iptables -F
sudo iptables -X

sudo iptables -t nat -F
sudo iptables -t nat -X

sudo iptables -t mangle -F
sudo iptables -t mangle -X

#Config new firewall
IPTABLES=/sbin/iptables
$IPTABLES -N internet -t mangle
$IPTABLES -t mangle -A PREROUTING -j internet
$IPTABLES -t mangle -A internet -j MARK --set-mark 99
$IPTABLES -t nat -A PREROUTING -m mark --mark 99 -p tcp --dport 80 -j DNAT --to-destination 192.168.5.1

echo "1" > /proc/sys/net/ipv4/ip_forward

$IPTABLES -A FORWARD -i eth0 -o wlan0 -m state --state ESTABLISHED,RELATED -j ACCEPT
$IPTABLES -A FORWARD -m mark --mark 99 -j REJECT
$IPTABLES -A FORWARD -i wlan0 -o eth0 -j ACCEPT
$IPTABLES -t nat -A POSTROUTING -o eth0 -j MASQUERADE

#Start Python script
>>>>>>> 90c0d4698f301bac546ac7058e085b90a4381803
sudo python server.py
