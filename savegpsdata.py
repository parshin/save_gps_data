#!/usr/bin/python
# -*- coding: utf-8

### BEGIN INIT INFO
# Provides:          savegpsdata
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start saving GPS data
# Description:       Start saving GPS data from arduino
### END INIT INFO

print 'listening...'
import socket
import MySQLdb
import datetime
import sys
from secrets import *

g_host = params["gpsdata"]["host"]
g_user = params["gpsdata"]["user"]
g_pass = params["gpsdata"]["passwd"]
g_db = params["gpsdata"]["db"]

UDP_IP = g_host
UDP_PORT = int(params["gpsdata"]["port"])


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

while  True:
	data, addr = sock.recvfrom(1024)
	#print "receive message: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data
	print "receive message: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	plat = data.find('lat')
	plon = data.find('lon')
	pcou = data.find('cou')
	palt = data.find('alt')
	pspd = data.find('spd')
	http = data.find('HTTP')
	if plat <> -1 and plon <> -1:
		lat = float(data[plat+4:plon-1])
		lon = float(data[plon+4:pcou-1])
		alt = int(data[palt+4:pspd-1])
		cou = int(data[pcou+4:palt-1])
		spd = int(data[pspd+4:http-1])
		print "lat:", lat
		print "lon:", lon
		print "cou:", cou
		print "alt:", alt
		print "spd:", spd
		if spd > 0:
			date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			# sql = """INSERT INTO coords(lat,lon,spd, date_time) 
			# VALUES ('%(flat)s', '%(flon)s', '%(fspd)s', '%(fdate_time)s')
			# """%{"flat":lat, "flon":lon, "fspd":spd, "fdate_time":date_time}
			sql = "INSERT INTO coords(lat,lon,alt,datetime,spd,cou) VALUES (%s,%s,%s,%s,%s,%s)"
			sql_params = (lat,lon,alt,date_time,spd,cou)
	
			try:
				db = MySQLdb.connect(host=g_host, user=g_user, passwd=g_pass, db=g_db,charset='utf8')
				cursor = db.cursor()
				cursor.execute(sql, sql_params)
				db.commit()
				cursor.close()
				db.close()
			except db.error as e:
				print db.error(), sys.exc_info()[0]
