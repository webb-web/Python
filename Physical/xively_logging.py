#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Adafruit_BMP085 import BMP085
import socket
import sys
import time
import math
import logging as log
import httplib
import json
import threading
log.basicConfig(level=log.INFO)

from ip_connection import IPConnection
from ip_connection import Error


class Xively:
    HOST = 'api.xively.com'
    AGENT = "swebb650"
    FEED = '208268878.json'
    API_KEY = 'Mo5YseQwnW19EZUsD1Y1bf2WWAPVqW8dlLIhJEFzfx9k8EIv'

    def __init__(self):
        self.items = {}
        self.headers = {
            "Content-Type"  : "application/x-www-form-urlencoded",
            "X-ApiKey"      : Xively.API_KEY,
            "User-Agent"    : Xively.AGENT,
        }
        self.params = "/v2/feeds/" + str(Xively.FEED)
        self.upload_thread = threading.Thread(target=self.upload)
        self.upload_thread.daemon = True
        self.upload_thread.start()

    def put(self, identifier, value):
        try:
            _, min_value, max_value = self.items[identifier]
            if value < min_value:
                min_value = value
            if value > max_value:
                max_value = value
            self.items[identifier] = (value, min_value, max_value)
        except:
            self.items[identifier] = (value, value, value)

    def upload(self):
        while True:
            time.sleep(60) # Upload data every 5min
            if len(self.items) == 0:
                continue

            stream_items = []
            for identifier, value in self.items.items():
                stream_items.append({'id': identifier,
                                     'current_value': value[0],
                                     'min_value': value[1],
                                     'max_value': value[2]})

            data = {'version': '1.0.0',
                    'datastreams': stream_items}
            self.items = {}
            body = json.dumps(data)

            try:
                http = httplib.HTTPSConnection(Xively.HOST)
                http.request('PUT', self.params, body, self.headers)
                response = http.getresponse()
                http.close()

                if response.status != 200:
                    log.error('Could not upload to xively -> ' +
                              str(response.status) + ': ' + response.reason)
            except Exception as e:
                log.error('HTTP error: ' + str(e))

class datalogging:
    HOST="localhost"
    PORT=4223
    ipcon=None
    
    def __init__(self):
        # [...]
        self.xively = Xively()
##        self.ipcon=IPConnection()
        while True:
            self.cb_temperature()
            self.cb_pressure()
            time.sleep(30)
##            try:
##                self.ipcon.connect(datalogging.HOST, datalogging.PORT)
##                break
##            except Error as e:
##                log.error('Connection Error: ' + str(e.description))
##                time.sleep(1)
##            except socket.error as e:
##                log.error('Socket error: ' + str(e))
##                time.sleep(1)
##
##        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE,
##                                     self.cb_enumerate)
##        self.ipcon.register_callback(IPConnection.CALLBACK_CONNECTED,
##                                     self.cb_connected)
##
##        while True:
##            try:
##                self.ipcon.enumerate()
##                break
##            except Error as e:
##                log.error('Enumerate Error: ' + str(e.description))
##                time.sleep(1)

    # [...]
    def cb_temperature(self):

        tfile = open ("/sys/bus/w1/devices/28-000004b63e35/w1_slave")
        texter = tfile.read()
        tfile.close()
        secondline =texter.split("\n")[1]
        tempdata=secondline.split(" ")[9]
        temperature=float(tempdata[2:])
        temperature=temperature/1000

        # Here we add temperature to Xively with ID "temperature_probe_DS18B20"
        self.xively.put('temperature_probe_DS18B20', temperature)
        log.info('Temperature: '+str(temperature))

    def cb_pressure(self):
        bmp = BMP085(0x77)
        pressure = bmp.readPressure()

        # Here we add presure to Xively with ID "barometric_pressure_BMP085"
        self.xively.put('barometric_pressure_BMP085', pressure)
        log.info('Pressure: '+str(pressure))

##    def cb_connected(self, connected_reason):
##        if connected_reason == IPConnection.CONNECT_REASON_AUTO_RECONNECT:
##            log.info('Auto Reconnect')
##
##            while True:
##                try:
##                    self.ipcon.enumerate()
##                    break
##                except Error as e:
##                    log.error('Enumerate Error: ' + str(e.description))
##                    time.sleep(1)
   
if __name__ == "__main__":
    log.info('Datalogging : Start')

    Data_Logging = datalogging()
##
##    if sys.version_info < (3, 0):
##        input = raw_input # Compatibility for Python 2.x
##    input('Press key to exit\n')
##
##    if Data_Logging.ipcon != None:
##        Data_Logging.ipcon.disconnect()

    log.info('Datalogging: End')
