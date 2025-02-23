import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)

def relay_on():
    GPIO.output(23, GPIO.HIGH)  
    print("Relay ON")

def relay_off():
    GPIO.output(23, GPIO.LOW)   
    print("Relay OFF")

try:
    while True:
        relay_on()
        time.sleep(2) 
        relay_off()  
        time.sleep(2) 
except KeyboardInterrupt:
    print("Program stopped by user")

GPIO.cleanup()
