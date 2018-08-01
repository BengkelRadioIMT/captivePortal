#!/bin/bash

sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
sudo iptables -t mangle -F
sudo iptables -t mangle -X
sudo iptables -N internet -t mangle
sudo iptables -t mangle -A PREROUTING -j internet
sudo iptables -t mangle -A internet -j MARK --set-mark 99
sudo iptables -t nat -A PREROUTING -m mark --mark 99 -p tcp --dport 80 -j DNAT --to-destination 192.168.5.1
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A FORWARD -m mark --mark 99 -j REJECT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
