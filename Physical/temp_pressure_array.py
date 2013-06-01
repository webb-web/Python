#!/usr/bin/python

from Adafruit_BMP085 import BMP085
import time
import datetime
from numpy import *
import csv

var = 0
sttime=time.time()
dataarray=zeros(4)
#converting time to GMT
st=datetime.datetime.fromtimestamp(sttime).strftime('%Y-%m-%d-%H-%M-%S')

#datafile = open ("/home/pi/Documents/temppress_data"+str(st)+".log", "w")


while var <10:
    #get time stamp 1 - time temp reading started in UTC
    ts1=time.time()

    #collect temperature reading
    tfile = open ("/sys/bus/w1/devices/28-000004b63e35/w1_slave")
    text = tfile.read()
    tfile.close()
    secondline =text.split("\n")[1]
    tempdata=secondline.split(" ")[9]
    temp=float(tempdata[2:])
    temp=temp/1000
    

    #get time stamp 2 - time temp reading finished and pressure started in UTC
    ts2=time.time()
    
    

    #collect pressure reading
    bmp = BMP085(0x77)
    pressure = bmp.readPressure()

    #get time stamp 3 - time pressure reading finished in UTC
    ts3=time.time()    

    #calculate best estimate of time
    tempdur=ts2-ts1
    pressdur= ts3-ts2
    temptime = ((ts2+ts1)/2)-sttime
    presstime = ((ts3+ts2)/2)-sttime
    
    #write data
    press=float(pressure)
    myarray =array([[temptime,temp,presstime,press]])
    dataarray=vstack((dataarray, myarray))
    
   #time between readings
    time.sleep(2)

    #move var to next loop
    var = var+1
    print var

#open csv file and write array   
print "writing data"
dataarray=delete(dataarray,0,0)
with open ('temppress_data'+str(st)+'.csv', 'wb') as csvfile:
    writer=csv.writer(csvfile, delimiter=' ')
    writer.writerow(('Temp time (s)', 'Temp (deg C)', 'Press time (s)', 'Press (Pa)'))
    writer.writerows(dataarray)

    

#datafile.write(dataarray)
#datafile.close()
print "finished"
