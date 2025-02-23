import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)  # Trig pin
GPIO.setup(22, GPIO.IN)   # Echo pin

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

try:
    while True:
        dist = get_distance()
        print(f"Distance: {dist:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()


