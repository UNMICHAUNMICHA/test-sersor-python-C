import RPi.GPIO as GPIO
import time
import cv2

#set pin 
GPIO.setmode(GPIO.BCM)
GPIO.setup(27 , GPIO.OUT) #un
GPIO.setup(22, GPIO.IN)  # un
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #infra
GPIO.setup(4, GPIO.OUT) #servo

pwn = GPIO.PWN(4, 50)
pwn.start(0)



def distance():
    GPIO.output(27, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(27 , GPIO.LOW)
    
    
    while GPIO.input(22) == GPIO.LOW:
        pluse_start = time.time()
        
    while GPIO.input(22) == GPIO.HIGH:
        pluse_end = time.time()
    
    pluse_duration = pluse_end - pluse_start
    
    distance = pluse_duration * 17150    
        
    return distance
    
    
def capture(cam):
    for i in range(10):
        start_time = time.time()
        ret, img = cam.read()
        end_time = time.time()

        time1 = end_time - start_time
        print(f"time : {time1:.4f}")
        
        if not ret:
            print("Not_save_img")
            return

        cv2.iwrite("img_" + ".jpg", img)
        time_img = time.time()
        time2 = time_img - start_time  
        print(f"time_img : {time2:.4f}")
        print(f"Save_img {i}")

        cv2.destroyAllWindows()
    
    
def main():
    
    print("open cam")
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpend():
        print("Cam not open")
        return
    
    while True:
        dist = distance()
        print(f"Distance : {dist:.2f} cm")
        
        
        if dist < 30:
            print("Deted with 30cm cam_img") 
            capture(cam)
            break
        time.sleep(0.1)
    
    GPIO.cleanup()
    cam.release()
    
   
    
if __name__ == "__main__":
    main()