#!/usr/bin/python
# -*- coding: utf-8
import socket

IPADDR = ""
PORT = ""

PACKETDATA = 'GET /test.php?lat=57.134948&lon=65.580741&cou=313&alt=72&spd=36 HTTP/1.0'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

s.connect((IPADDR, PORT))

s.send(PACKETDATA)
s.close()
