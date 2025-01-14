import time
import spidev

# Thermocouple Acquisition Circuit Configuration
CS_PIN = 0  # GPIO 7


def setup_spi():
    """
    Initialize the SPI bus and configure its parameters.
    """
    spi = spidev.SpiDev()
    spi.open(0, 0)  # Open SPI bus 1, device 0
    spi.max_speed_hz = 1350000  # Set SPI clock speed
    spi.mode = 0b00  # Set SPI mode (CPOL=0, CPHA=0)
    spi.bits_per_word = 8  # Set SPI word size to 8 bits
    return spi


def read_thermocouple(spi):
    """
    Read and decode data from the thermocouple.
    """
    # Send dummy bytes to trigger SPI read
    response = spi.xfer2([0x00, 0x00, 0x00, 0x00])

    # Combine bytes into a single 32-bit integer
    raw_data = (response[0] << 24) | (response[1] << 16) | (response[2] << 8) | response[3]

    # Extract the temperature and status from raw_data
    # Assuming:
    # - Bits 31:18 are unused or reserved
    # - Bits 17:4 contain temperature data (12-bit value)
    # - Bits 3:0 contain error/status flags
    temperature_data = (raw_data >> 4) & 0xFFF  # Extract 12-bit temperature data
    status_flags = raw_data & 0xF  # Extract 4-bit status flags

    # Convert temperature data to Celsius (example scale: 0.25 °C per LSB)
    temperature = temperature_data * 0.25

    return temperature, status_flags


def main():
    """
    Main loop to read thermocouple data.
    """
    spi = setup_spi()
    try:
        while True:
            temperature, status_flags = read_thermocouple(spi)
            print(f"Temperature: {temperature:.2f} °C, Status Flags: {status_flags:#04x}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        spi.close()


if __name__ == "__main__":
    main()
