import time

import spidev

# Thermocouple Acquisition Circuit Configuration
CS_PIN = 0  # GPIO 7


def setup_spi():
    """
    Initialize the SPI bus and configure its parameters.
    """
    spi = spidev.SpiDev()
    spi.open(0, 0)  # Open SPI bus 0, device 0
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

    # Extract and decode 14-bit thermocouple temperature data (bits 31:18)
    thermocouple_data = (raw_data >> 18) & 0x3FFF  # Mask to 14 bits
    if thermocouple_data & 0x2000:  # Check if sign bit (bit 13) is set
        thermocouple_data -= 0x4000  # Convert to signed value
    thermocouple_temperature = thermocouple_data * 0.25  # Scale to Celsius

    # Extract fault bit (bit 16)
    fault = (raw_data >> 16) & 0x1

    # Extract and decode 12-bit internal temperature data (bits 15:4)
    internal_data = (raw_data >> 4) & 0xFFF  # Mask to 12 bits
    if internal_data & 0x800:  # Check if sign bit (bit 11) is set
        internal_data -= 0x1000  # Convert to signed value
    internal_temperature = internal_data * 0.0625  # Scale to Celsius

    # Extract status flags (bits 3:0)
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


def main():
    """
    Main loop to read thermocouple data.
    """
    spi = setup_spi()
    try:
        while True:
            data = read_thermocouple(spi)
            print(f"Thermocouple Temperature: {data['thermocouple_temperature']:.2f} °C")
            print(f"Internal Temperature: {data['internal_temperature']:.2f} °C")
            print(f"Fault: {data['fault']}, SCV: {data['scv_fault']}, SCG: {data['scg_fault']}, OC: {data['oc_fault']}")
            print("----------------------------------------")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        spi.close()


if __name__ == "__main__":
    main()
