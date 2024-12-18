import spidev
import time

# MCP3004 Configuration
CS_PIN = 8  # GPIO 8


def setup_spi():
    spi = spidev.SpiDev()
    spi.open(0, CS_PIN)  # Open SPI bus 0 and the CS_PIN as the chip select
    spi.max_speed_hz = 1350000  # Set SPI clock speed
    return spi


def read_adc_channel(spi, channel):
    if channel < 0 or channel > 3:
        raise ValueError("Channel must be between 0 and 3 for MCP3004.")

    # Construct the command byte for MCP3004
    cmd = [1, (8 + channel) << 4, 0]
    response = spi.xfer2(cmd)

    # Extract the 10-bit ADC value
    adc_value = ((response[1] & 3) << 8) + response[2]
    return adc_value


def main():
    spi = setup_spi()
    try:
        while True:
            channel = int(input("Enter MCP3004 channel (0-3): "))
            value = read_adc_channel(spi, channel)
            print(f"ADC Channel {channel} Value: {value}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        spi.close()


if __name__ == "__main__":
    main()
