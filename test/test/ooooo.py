import serial
import time

# กำหนดพอร์ตและความเร็ว Baud rate ให้ตรงกับ Arduino
# ทั่วไปใน RPi จะเป็น '/dev/ttyUSB0' หรือ '/dev/ttyACM0'
serial_port = '/dev/ttyACM0'  # อาจต้องเปลี่ยนตามพอร์ตที่ใช้จริง
baud_rate = 9600  # ต้องตรงกับ Serial.begin(9600) ใน Arduino

try:
    # สร้าง object สำหรับ serial communication
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    # รอให้การเชื่อมต่อเสถียร
    time.sleep(2)
    print("Connected to Arduino successfully")

    while True:
        # อ่านข้อมูลจาก serial
        if ser.in_waiting > 0:  # ตรวจสอบว่ามีข้อมูลรออยู่หรือไม่
            data = ser.readline().decode('utf-8').strip()  # อ่านและแปลงเป็น string
            
            # ตรวจสอบข้อมูลที่ได้รับ
            if data == "1":
                print("1")
            elif data == "0":
                print("0")
            else:
                print(f"Received unexpected data: {data}")
                
        time.sleep(0.1)  # delay เล็กน้อยเพื่อไม่ให้ CPU ทำงานหนักเกิน

except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("\nProgram terminated by user")
finally:
    if 'ser' in locals():
        ser.close()  # ปิดการเชื่อมต่อ serial
        print("Serial connection closed")
