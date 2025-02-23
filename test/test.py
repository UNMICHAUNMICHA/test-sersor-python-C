import serial
import time

# เชื่อมต่อกับพอร์ตที่ Arduino ใช้
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# รอให้การเชื่อมต่อกับ Arduino พร้อม
time.sleep(2)

while True:
    # อ่านค่าจาก Serial
    if arduino.in_waiting > 0:
        distance = arduino.readline().decode('utf-8').strip()
        print(f"Distance: {distance} cm")
    
    time.sleep(1)
