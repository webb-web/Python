import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11,False)
var = 1
while var<10:
    input_value=GPIO.input(12)
    if input_value == True:
        print("The Button was pressed. Lighting LED")
        GPIO.output(11,True)
        var = var +1
        while input_value == True:
            input_value=GPIO.input(12)
        print ("The button has been released, Extinguishing LED.")

    if input_value == False:
        GPIO.output(11, False)
GPIO.cleanup()
exit()
