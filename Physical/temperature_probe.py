#import RPi.GPIO

var = 0
datafile = open ("tempdata.log", "w")

while var <10:
    tfile = open ("/sys/bus/w1/devices/28-000004b63e35/w1_slave")
    text = tfile.read()
    tfile.close()
    secondline =text.split("\n")[1]
    tempdata=secondline.split(" ")[9]
    temp=float(tempdata[2:])
    temp=temp/1000
    print temp
    datafile.write(str(temp) + "\n")
    var = var+1

datafile.close()
#exit()
    
