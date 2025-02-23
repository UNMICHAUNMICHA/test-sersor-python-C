import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)  # Trig pin for Ultrasonic sensor
GPIO.setup(22, GPIO.IN)   # Echo pin for Ultrasonic sensor

GPIO.setup(4, GPIO.OUT)   # Servo control pin

# Setup PWM for servo motor
pwm = GPIO.PWM(4, 50) 
pwm.start(0)

def get_distance():
    GPIO.output(27, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(27, GPIO.LOW)

    while GPIO.input(22) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(22) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150  

    return distance

def move_servo():
    for angle in range(0, 181, 10):  
        duty = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)

    time.sleep(1) 

    for angle in range(180, -1, -10): 
        duty = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)

    pwm.ChangeDutyCycle(0) 

try:
    while True:
        dist = get_distance()
        print(f"Distance: {dist:.2f} cm")
        
        if dist < 30:
            print("Object detected within 30 cm! Moving servo...")
            move_servo()
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    pwm.stop()
    GPIO.cleanup()





