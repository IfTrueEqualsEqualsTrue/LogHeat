import serial
import time


ser = serial.Serial('COM5', 9600, timeout=1)

time.sleep(1)

try:
    while True:

        line = ser.readline().decode('utf-8').strip()

        if line:
            print(f"Temperature: {line}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting Program")

finally:
    ser.close()
