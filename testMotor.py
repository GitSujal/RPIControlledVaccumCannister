import RPi.GPIO as GPIO           # import RPi.GPIO module  
import time



GPIO.setmode(GPIO.BCM)   
# For Vaccum Pump
GPIO.setup(26, GPIO.OUT) # set a port/pin as an output 

while True:


    GPIO.output(26, 1)       # set port/pin value to 1/GPIO.HIGH/True  

    time.sleep(5)

    GPIO.output(26, 0) 

    time.sleep(5)