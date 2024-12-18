import time

import spidev

# MCP3004 Configuration
CS_PIN = 8  # GPIO 8 (You may not need to specify this, use 0, 0 instead)


def setup_spi():
    spi = spidev.SpiDev()
    spi.open(0, 0)  # Open SPI bus 0, device 0 (chip select managed automatically)
    spi.max_speed_hz = 1000000  # Set SPI clock speed to 1 MHz (safe range for MCP3004)
    spi.mode = 0  # Ensure SPI mode is 0 (CPOL = 0, CPHA = 0)
    return spi


def read_adc_channel(spi, channel):
    if channel < 0 or channel > 3:
        raise ValueError("Channel must be between 0 and 3 for MCP3004.")

    # Construct the command byte for MCP3004
    cmd = [1, (8 + channel) << 4, 0]
    print(f"Sending Command: {cmd}")  # Debug: Print the command byte
    response = spi.xfer2(cmd)
    print(f"SPI Response: {response}")  # Debug: Print the response bytes

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
