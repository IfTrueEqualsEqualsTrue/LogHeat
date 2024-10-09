""" Tools for writing on a virtual com port in order to test the software without the need for hardware.
Create virtual com port pair with https://freevirtualserialports.com/"""

import threading

import serial
import time
import random


class COMPortSimulator:
    def __init__(self, port, baudrate, frequency):
        self.port = port
        self.baudrate = baudrate
        self.frequency = frequency
        self.ser = serial.Serial(port, baudrate)

    @staticmethod
    def generate_data():
        return f"{random.randint(0, 500)}\n"

    def run(self):
        while True:
            data = self.generate_data()
            print(f'Sent : {data}\n')
            self.ser.write(data.encode())
            time.sleep(1 / self.frequency)


class COMPortReader:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)

    def run(self):
        while True:
            data = self.ser.read(100)
            if data:
                print(f"Received: {data.decode()}", end='')


if __name__ == "__main__":
    simulator = COMPortSimulator('COM1', 9600, 0.3)  # Adapt the writing and reading
    reader = COMPortReader('COM2', 9600)

    simulator_thread = threading.Thread(target=simulator.run)
    reader_thread = threading.Thread(target=reader.run)

    simulator_thread.start()
    reader_thread.start()

    simulator_thread.join()
    reader_thread.join()
