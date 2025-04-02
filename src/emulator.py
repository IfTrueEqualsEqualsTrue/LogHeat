""" This file contains utilities to run the project without the need for a real COM port. Make sure to setup a virtual
COM bridge accordingly to the write_port and read_port variables. When using this emulator, the interface shouldn't use
the SpiReader class, but the COMPortReader class instead. """

import logging
import queue
import random
import threading
import time

import serial

logging.basicConfig(level=logging.DEBUG)

write_port = 'COM1'
read_port = 'COM2'
frequency = 0.5
bdrate = 9600


class COMPortSimulator:
    def __init__(self, port, baudrate, frequency):
        self.port = port
        self.baudrate = baudrate
        self.frequency = frequency
        self.ser = serial.Serial(port, baudrate)
        self.is_running = False
        self.thread = None

    @staticmethod
    def generate_data():
        return f"{random.randint(0, 500)}\n"

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()

    def run(self):
        while self.is_running:
            try:
                data = self.generate_data()
                print(f'Sent : {data}\n')
                self.ser.write(data.encode())
            except serial.SerialException as e:
                logging.error(f"Serial port error: {e}")
            time.sleep(1 / self.frequency)


class COMPortReader:
    def __init__(self, queue=queue.Queue(), port=read_port, baudrate=bdrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        self.is_running = False
        self.thread = None
        self.data_queue = queue

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()

    def run(self):
        while self.is_running:
            try:
                data = self.ser.read(100)
                if data:
                    self.data_queue.put(data.decode())
            except serial.SerialException as e:
                logging.error(f"Serial port error: {e}")

    def get_data(self):
        if not self.data_queue.empty():
            return self.data_queue.get()
        return None


def start_emulation():
    simulator = COMPortSimulator(write_port, bdrate, frequency)
    simulator.start()
    print("Emulation started.")


def stop_emulation():
    simulator = COMPortSimulator(write_port, bdrate, frequency)
    simulator.stop()
    print("Emulation stopped.")


def test_emulation():
    simulator = COMPortSimulator(write_port, bdrate, frequency)
    reader = COMPortReader(read_port, bdrate)

    simulator.start()
    reader.start()

    try:
        while True:
            data = reader.get_data()
            if data:
                print(f"Received: {data}", end='')
            time.sleep(0.1)  # Small delay to prevent busy-waiting
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        simulator.stop()
        reader.stop()


start_emulation()
