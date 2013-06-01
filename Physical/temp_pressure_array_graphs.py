#_*_ coding:utf-8 _*_
#!/usr/bin/python

from Adafruit_BMP085 import BMP085
import time
import datetime
from numpy import *
import csv
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pylab

var = 0
sttime=time.time()
dataarray=zeros(4)
#converting time to GMT
st=datetime.datetime.fromtimestamp(sttime).strftime('%Y-%m-%d-%H-%M-%S')

#datafile = open ("/home/pi/Documents/temppress_data"+str(st)+".log", "w")


while var <20:
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

    #calculate best estimate of times
    tempdur=ts2-ts1
    pressdur= ts3-ts2
    temptime = ((ts2+ts1)/2)-sttime
    presstime = ((ts3+ts2)/2)-sttime
    
    #write data to array
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
    writer.writerow(('Temptime (s)', u'Temperature (\N{DEGREE SIGN}C)', 'Presstime (s)', 'Pressure (Pa)'))
    writer.writerows(dataarray)

#create graph
print "drawing graph"
col_names=('Temptime','Temp','Presstime','Press')
r=mlab.csv2rec('temppress_data'+str(st)+'.csv', skiprows=1,delimiter=' ', names=col_names)
f, ax = plt.subplots(2, sharex=True)
ax[0].set_title("Graph of temperature and pressure against time", fontsize=14)
#ax[0].set_xlabel("time (s)", fontsize=12)
ax[0].set_ylabel(u"Temperature (\N{DEGREE SIGN}C)", fontsize=12)
ax[0].grid(True, linestyle='-', color='0.75')
ax[0].scatter(r['Temptime'], r['Temp'], s=20, color='tomato');
ax[1].set_xlabel("time (s)", fontsize=12)
ax[1].set_ylabel("Pressure (Pa)", fontsize=12)
ax[1].grid(True, linestyle='-', color='0.75')
ax[1].scatter(r['Presstime'], r['Press'], s=20, color='tomato');
pylab.savefig('temppress_data'+str(st)+'.png',bbox_inches=0,dpi=100)
pylab.show()

print "finished"
