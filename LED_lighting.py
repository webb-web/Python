import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
var=1
while var <5:
    GPIO.output(11,False)
    time.sleep(2)
    GPIO.output(11, False)
    time.sleep(2)
    print (var)
    var=var+1
GPIO.cleanup()
exit()
