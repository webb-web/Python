#!/usr/bin/python

from Adafruit_BMP085 import BMP085
import time
import datetime

var = 0
datafile = open ("/home/pi/Documents/temppress_data.log", "w")
datafile.write(str("Time Stamp")+"\t"+str("Temperature")+"\t"+ str("Pressure")+ "\n")

while var <10:
    #tempdata
    tfile = open ("/sys/bus/w1/devices/28-000004b63e35/w1_slave")
    text = tfile.read()
    tfile.close()
    secondline =text.split("\n")[1]
    tempdata=secondline.split(" ")[9]
    temp=float(tempdata[2:])
    temp=temp/1000
    #print temp
    

    #get time stamp
    st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

    #pressure data
    bmp = BMP085(0x77)
    pressure = bmp.readPressure()
    #print pressure
    time.sleep(2)
    var = var+1

    #write date
    datafile.write(str(ts) + "\t")
    datafile.write(str(temp) + "\t")
    datafile.write(str(pressure) + "\n")

datafile.close()
