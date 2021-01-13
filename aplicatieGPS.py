import serial
import os
import math
import numpy as np
import os
import time

os.system("sudo systemctl stop gpsd.socket")
time.slee(0.1)
os.system("sudo gpsd /dev/ttyS0 -N -D3 -F /var/run/gpsd.sock^C")
time.slee(0.1)

class GPS:
    def __init__(self):
        self.gps = serial.Serial("/dev/ttyS0", baudrate=9600)
        self.R = 6371000

    def coord_to_meters(self, lat1, long1, lat2, long2):
        delta_lat = lat2 - lat1
        delta_long = long2 - long1
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_long / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return (self.R * c)

    def get_pozitie(self):
        ok1 = ok2 = 0
        while True:
            try:
                line = self.gps.readline().decode("utf-8")
            except UnicodeDecodeError:
                fail = 1
                continue
            if line[0:6] == "$GNGGA":
                try:
                    altitude = float(line[52:57].strip(','))
                    ok1 = 1
                except ValueError:
                    continue
            if line[0:6] == "$GNRMC":
                try:
                    lat = line[20:29]
                    longi = line[32:42]
                    print(lat, longi)
                    # v2 = float(line[45:49])*0.5144447
                    lat = float(lat[0:2]) * math.pi / 180 + (float(lat[2:9]) / 60) * math.pi / 180
                    longi = float(longi[0:3]) * math.pi / 180 + (float(longi[3:10]) / 60) * math.pi / 180
                    ok2 = 1
                except ValueError:
                    continue
            if ok1 == 1 and ok2 == 1:
                break
        return lat, longi, altitude

