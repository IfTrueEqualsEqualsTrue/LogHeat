import time

import spidev

SPI_BUS = 0
CS_PIN = 1


def setup_spi():
    spi = spidev.SpiDev()
    spi.open(SPI_BUS, CS_PIN)
    spi.max_speed_hz = 500000
    return spi


def read_adc_channel(spi, channel):
    if channel < 0 or channel > 3:
        raise ValueError("Channel must be between 0 and 3 for MCP3004.")

    # Construction de la commande SPI
    cmd = [0b01, (0b1000 | (channel << 4)), 0x00]
    response = spi.xfer2(cmd)

    # Extraction des données sur 10 bits
    adc_value = ((response[1] & 0b11) << 8) | response[2]
    return adc_value


def main():
    spi = setup_spi()
    try:
        while True:
            for channel in range(4):  # Lecture automatique des 4 canaux
                value = read_adc_channel(spi, channel)
                print(f"ADC Channel {channel} Value: {value}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        spi.close()


if __name__ == "__main__":
    main()
