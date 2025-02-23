import serial
import time

# กำหนดพอร์ตที่เชื่อมต่อกับ Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # แทนที่ '/dev/ttyUSB0' ด้วยพอร์ตที่ใช้งานจริง

time.sleep(2)  # รอให้ Arduino เริ่มทำงาน

# ส่งข้อมูลไปยัง Arduino
arduino.write(b'Hello from RPi\n')

# ปิดการเชื่อมต่อ
arduino.close()
