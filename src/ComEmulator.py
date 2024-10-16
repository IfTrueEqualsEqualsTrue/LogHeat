import logging
import queue
import random
import threading
import time
import serial

logging.basicConfig(level=logging.ERROR)

write_port = 'COM1'
read_port = 'COM2'
frequency = 5
bdrate = 9600


class COMPortSimulator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(COMPortSimulator, cls).__new__(cls)
        return cls._instance

    def __init__(self, port, baudrate, frequency):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.port = port
            self.baudrate = baudrate
            self.frequency = frequency
            self.ser = serial.Serial(port, baudrate)
            self.is_running = False
            self.thread = None
            self.initialized = True

    @staticmethod
    def generate_data():
        return f"{random.randint(0, 500)}\n"

    def start(self):
        if not self.is_running:
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

    @classmethod
    def get_instance(cls):
        return cls(write_port, bdrate, frequency)


class COMPortReader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(COMPortReader, cls).__new__(cls)
        return cls._instance

    def __init__(self, port, baudrate):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.port = port
            self.baudrate = baudrate
            self.ser = serial.Serial(port, baudrate)
            self.is_running = False
            self.thread = None
            self.data_queue = queue.Queue()
            self.initialized = True

    def start(self):
        if not self.is_running:
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
                data = self.ser.readline().decode('utf-8').strip()  # strip removes trailing \r\n
                if data:
                    try:
                        temperature = float(data)
                        self.data_queue.put(temperature)
                    except ValueError:
                        logging.error(f"Invalid data received: {data}")  # Handle any non-float data
            except serial.SerialException as e:
                logging.error(f"Serial port error: {e}")

    def get_data(self):
        if not self.data_queue.empty():
            return self.data_queue.get()
        return None

    @classmethod
    def get_instance(cls):
        return cls(read_port, bdrate)


def start_emulation():
    simulator = COMPortSimulator.get_instance()
    simulator.start()
    print("Emulation started.")


def stop_emulation():
    simulator = COMPortSimulator.get_instance()
    simulator.stop()
    print("Emulation stopped.")


def test_emulation():
    simulator = COMPortSimulator.get_instance()
    reader = COMPortReader.get_instance()

    simulator.start()
    reader.start()

    try:
        while True:
            data = reader.get_data()
            if data:
                print(f"Received: {data}", end='')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        simulator.stop()
        reader.stop()
