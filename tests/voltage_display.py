import serial
import time

ser = serial.Serial('COM5', 9600, timeout=1)
ser.flush()
moy = 0
tot = 0
i = 1
while True:

    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        voltages = line.split(',')
        if len(voltages) == 2:
            tot += float(voltages[0])
            moy = tot / i
            print(f"Voltage 1: {voltages[0]}V")
            print(f"Voltage 2: {voltages[1]}V")
            print(f"moy : {moy:.2f}V")
            print(f'Difference : {float(voltages[1])-float(voltages[0]):.2f} V')
            print("--------------------")
            i += 1
    time.sleep(1)
