import RPi.GPIO as GPIO           # import RPi.GPIO module  
import time

GPIO.setmode(GPIO.BCM)   
# For Vaccum Pump
GPIO.setup(26, GPIO.IN) # set a port/pin as an output 

