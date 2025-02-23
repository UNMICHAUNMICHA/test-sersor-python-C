import serial
import time
import cv2

def reinitialize_arduino():
    global arduino
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(3)
        print("Reinitialized Arduino connection")
    except serial.SerialException as e:
        print(f"Failed to reinitialize Arduino: {e}")
        arduino = None

def safe_arduino_write(command):
    try:
        arduino.write(command)
        arduino.flush()  
    except serial.SerialException as e:
        print(f"Error during serial communication: {e}")
        arduino.close()  
        time.sleep(2)
        reinitialize_arduino() 

def relay_on():
    print("Turning relay ON...")
    safe_arduino_write(b"relay_on\n")

def relay_off():
    print("Turning relay OFF...")
    safe_arduino_write(b"relay_off\n")

def move_servo(angle):
    try:
        arduino.write(f"move_servo {angle}\n".encode())
        arduino.flush()  
        print(f"Moving servo to {angle} degrees")
    except serial.SerialException as e:
        print(f"Error while moving servo: {e}")

def capture_image(cam):
    for i in range(5):
        start_time = time.time()
        ret, image = cam.read()  
        end_time = time.time()

        if not ret:
            print("Not_save_img") 
            return

        filename = f"img_{i}.jpg"
        cv2.imwrite(filename, image) 
        print(f"Saved {filename}")

    cv2.destroyAllWindows()

def read_distance_from_arduino():
    try:
        if arduino.in_waiting > 0:
            distance = arduino.readline().decode('utf-8', errors='ignore').strip()
            if distance == "READY":
                return "READY"  # Indicates Arduino is ready for the next task
            return distance
        else:
            return None
    except serial.SerialException as e:
        print(f"Error while reading data: {e}")
        reinitialize_arduino()  
        return None

def main():
    reinitialize_arduino()

    if arduino is None:
        print("Failed to initialize Arduino. Exiting...")
        return

    relay_on()
    print("Starting...")

    cam = cv2.VideoCapture(0)

    if not cam.isOpened(): 
        print("Camera not open")
        return

    try:
        while True:
            distance = read_distance_from_arduino()

            if distance:
                print(f"Distance: {distance} cm")

                if distance == "READY":
                    print("Arduino is ready for the next operation.")
                    continue  # Wait for Arduino to be ready for the next operation

                if "Distance:" in distance:
                    distance = distance.replace("Distance:", "").strip()

                try:
                    distance_value = float(distance)
                    if distance_value < 27.5 or distance_value > 32:
                        print("Capturing image...")
                        capture_image(cam)
                        move_servo(50)
                        time.sleep(2)
                except ValueError:
                    print(f"Invalid distance value received: {distance}. Skipping...")
            
            time.sleep(0.1)  # Wait a little before checking the distance again

    finally:
        relay_off()
        cam.release()

if __name__ == "__main__":
    main()
    