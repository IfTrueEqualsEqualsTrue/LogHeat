# import spidev
import threading
import queue
import time


class SPIReader(threading.Thread):
    def __init__(self, data_queue, spi_bus=0, spi_device=0, max_speed_hz=1350000):
        super().__init__()
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = 0b00
        self.spi.bits_per_word = 8
        self.data_queue = data_queue
        self.running = True

    def run(self):
        while self.running:
            data = self.read_thermocouple()
            self.data_queue.put(data)
            time.sleep(0.5)

    def read_thermocouple(self):
        response = self.spi.xfer2([0x00, 0x00, 0x00, 0x00])
        raw_data = (response[0] << 24) | (response[1] << 16) | (response[2] << 8) | response[3]
        thermocouple_data = (raw_data >> 18) & 0x3FFF
        if thermocouple_data & 0x2000:
            thermocouple_data -= 0x4000
        thermocouple_temperature = thermocouple_data * 0.25
        fault = (raw_data >> 16) & 0x1
        internal_data = (raw_data >> 4) & 0xFFF
        if internal_data & 0x800:
            internal_data -= 0x1000
        internal_temperature = internal_data * 0.0625
        scv_fault = (raw_data >> 2) & 0x1
        scg_fault = (raw_data >> 1) & 0x1
        oc_fault = raw_data & 0x1
        return {
            "thermocouple_temperature": thermocouple_temperature,
            "internal_temperature": internal_temperature,
            "fault": fault,
            "scv_fault": scv_fault,
            "scg_fault": scg_fault,
            "oc_fault": oc_fault
        }

    def stop(self):
        self.running = False
        self.spi.close()
