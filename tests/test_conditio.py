import time

import spidev

# Thermocouple Acquisition Circuit Configuration
CS_PIN = 7  # GPIO 7


def setup_spi():
    spi = spidev.SpiDev()
    spi.open(0, CS_PIN)  # Open SPI bus 0 and the CS_PIN as the chip select
    spi.max_speed_hz = 1350000  # Set SPI clock speed
    return spi


def read_thermocouple(spi):
    # Send a dummy byte to read data
    response = spi.xfer2([0x00, 0x00, 0x00, 0x00])
    # Combine the bytes to extract the data
    raw_data = (response[0] << 24) | (response[1] << 16) | (response[2] << 8) | response[3]
    # Parse the raw data (modify this according to your acquisition circuit's protocol)
    return raw_data


def main():
    spi = setup_spi()
    try:
        while True:
            value = read_thermocouple(spi)
            print(f"Thermocouple Raw Data: {value}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        spi.close()


if __name__ == "__main__":
    main()
