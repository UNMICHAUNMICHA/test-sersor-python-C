import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)  # Trig pin for Ultrasonic sensor
GPIO.setup(22, GPIO.IN)   # Echo pin for Ultrasonic sensor

GPIO.setup(4, GPIO.OUT)   # Servo control pin

# Setup PWM for servo motor
pwm = GPIO.PWM(4, 50)  # 50Hz for servo motor
pwm.start(0)

def get_distance():
    # Send a pulse to the trig pin
    GPIO.output(27, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(27, GPIO.LOW)

    # Wait for the Echo pin to go HIGH and start timing
    while GPIO.input(22) == GPIO.LOW:
        pulse_start = time.time()

    # Wait for Echo to go LOW and stop timing
    while GPIO.input(22) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Calculate the distance (speed of sound = 34300 cm/s)
    distance = pulse_duration * 17150  # Divide by 2 (round-trip) and convert to cm

    return distance

def move_servo():
    # Move servo from 0 to 180 degrees and back to 0
    for angle in range(0, 181, 10):  # Increase angle from 0 to 180
        duty = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)

    time.sleep(1)  # Hold at 180 degrees

    for angle in range(180, -1, -10):  # Decrease angle from 180 to 0
        duty = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)

    pwm.ChangeDutyCycle(0)  # Stop the servo from moving

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





