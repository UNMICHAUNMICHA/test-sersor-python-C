import RPi.GPIO as GPIO
import time
import cv2

# Set up GPIO for Ultrasonic sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)  # Trig pin for Ultrasonic sensor
GPIO.setup(22, GPIO.IN)   # Echo pin for Ultrasonic sensor
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO for camera trigger (Button)

# Set up GPIO for Servo (if you need to include the servo control)
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

def capture_image(cam):
    for i in range(10):
        start_time = time.time()
        ret, image = cam.read()
        end_time = time.time()
        
        time1 = end_time - start_time
        print(f"time : {time1:.4f}")
        
        if not ret:
            print("Not_save_img")
            return
        
        cv2.imwrite("img_" + str(i) +".jpg", image)
        time_img_save = time.time()
        time2 = time_img_save - start_time
        print(f"time_img : {time2:.4f}")
        print(f"Save_img {i}")

        cv2.destroyAllWindows()

def main():
    print("Starting...")
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Camera not open")
        return
    
    while True:
        # Measure the distance from the Ultrasonic sensor
        dist = get_distance()
        print(f"Distance: {dist:.2f} cm")
        
        if dist < 30:  # If the distance is less than 30 cm
            print("Object detected within 30 cm! Capturing image...")
            capture_image(cam)  # Call the capture image function
            break  # Exit the loop after capturing the image

        time.sleep(0.1)  # Wait a bit before checking the distance again
    
    GPIO.cleanup()  # Clean up GPIO
    cam.release()  # Release the camera

if __name__ == "__main__":
    main()
