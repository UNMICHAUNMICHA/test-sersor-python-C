import RPi.GPIO as GPIO
import time
import cv2

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT) 
GPIO.setup(22, GPIO.IN)  
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(23, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)   
pwm = GPIO.PWM(4, 50) 
pwm.start(0)


def relay_on():
    GPIO.output(23, GPIO.HIGH)
    print("relay ON")

def relay_off():
    GPIO.output(23, GPIO.LOW)
    print("relay OFF")

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

def get_average_distance(num_samples=1):
    distances = []
    
    for _ in range(num_samples):
        dist = get_distance()  
        distances.append(dist) 
        time.sleep(0.05)  
    
    avg_dist = sum(distances) / len(distances)  
    time.sleep(5)
    return avg_dist

def move_servo(angle):
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5) 
    pwm.ChangeDutyCycle(0)

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
    relay_on()
    move_servo(180)
    print("Starting...")
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Camera not open")
        return
    
    try:
        while True: 
            avg_dist = get_average_distance() 
            print(f"Distance: {avg_dist:.2f} cm")
            
            if avg_dist < 28.7 or avg_dist > 34: 
                print("Object detected within 29 cm! Capturing image...")
                capture_image(cam) 
                move_servo(180)
                time.sleep(1)
                move_servo(30)
                time.sleep(1)
         
            time.sleep(0.1)
    finally:
        relay_off()
        GPIO.cleanup()  
        cam.release()

if __name__ == "__main__":
    main()
