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

import SocketServer
from secrets import *
import MySQLdb
import datetime
#import sys

USER = params["gpsdata"]["user"]
PASS = params["gpsdata"]["passwd"]
DBNM = params["gpsdata"]["db"]
HOST = params["gpsdata"]["host"]
HOSTDB = params["gpsdata"]["hostdb"]
PORT = int(params["gpsdata"]["port"])

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        #print "{} wrote:".format(self.client_address[0])
        #print data
        #socket.sendto(data.upper(), self.client_address)
        #print "{} wrote".format(self.client_address[0]) + " at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plat = data.find('lat')
        plon = data.find('lon')
        pcou = data.find('cou')
        palt = data.find('alt')
        pspd = data.find('spd')
#        http = data.find('HTTP')
        if plat <> -1 and plon <> -1:
            lat = float(data[plat+4:plon-1])
            lon = float(data[plon+4:pcou-1])
            alt = int(data[palt+4:pspd-1])
            cou = int(data[pcou+4:palt-1])
            spd = int(data[pspd+4:pspd+7])
            #print "lat:", lat
            #print "lon:", lon
            #print "cou:", cou
            #print "alt:", alt
            #print "spd:", spd
            #if spd > 0:
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # sql = """INSERT INTO coords(lat,lon,spd, date_time) 
            # VALUES ('%(flat)s', '%(flon)s', '%(fspd)s', '%(fdate_time)s')
            # """%{"flat":lat, "flon":lon, "fspd":spd, "fdate_time":date_time}
            sql = "INSERT INTO coords(lat,lon,alt,datetime,spd,cou) VALUES (%s,%s,%s,%s,%s,%s)"
            sql_params = (lat,lon,alt,date_time,spd,cou)
    
            try:
                db = MySQLdb.connect(host=HOSTDB, user=USER, passwd=PASS, db=DBNM, charset='utf8')
                cursor = db.cursor()
                cursor.execute(sql, sql_params)
                db.commit()
                cursor.close()
                db.close()
            #except db.error as e:
            #    print db.error(), sys.exc_info()[0]
            except MySQLdb.Error, e:
            #    print "Error %d: %s" % (e.args[0], e.args[1])
                ""


if __name__ == "__main__":
    #print 'waiting for data...'
    #HOST, PORT = "localhost", 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
