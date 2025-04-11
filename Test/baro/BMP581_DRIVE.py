import smbus2
import time

# I2C address of the BMP581 sensor
BMP581_I2C_ADDRESS = 0x47  # Replace with your sensor's address if different

# Registers (replace with actual BMP581 register addresses from the datasheet)
BMP581_CHIP_ID_REG = 0x01       # Example: Chip ID register
BMP581_PRESSURE_REG = 0x20      # Example: Pressure data register
BMP581_TEMPERATURE_REG = 0x1D   # Example: Temperature data register
BMP581_OSR_REG = 0x36           # Example: Oversampling register
BMP581_ODR_REG = 0x37           # Example: Output Data Rate register

# Initialize the I2C bus
bus = smbus2.SMBus(1)  # Use I2C bus 1 (check your hardware setup)

class BMP581:
    def __init__(self):
        try:
            # Read the chip ID from the BMP581 sensor.
            chip_id = self.read_register(BMP581_CHIP_ID_REG, 1)[0]
            if chip_id != 0x50:  # Replace with the expected chip ID
                print(f"Unexpected chip ID: {chip_id:#X}")
                self.chip_id = None
            else:
                print(f"Chip ID: {chip_id:#X}")
                self.chip_id = chip_id

            # Configure Oversampling (example values, check the datasheet)
            # OSR_REG = <reserved_7: 1bit> | <prss_en: 1bit> | <osr_p: 3bits> | <osr_t: 3bits>
            self.write_register(BMP581_OSR_REG, 0b01001001)  # Set oversampling

            # Configure Output Data Rate(ODR) (example values, check the datasheet)
            # ODR_REG = <deep_dis: 1bit> | <odr: 5bits> | <pwr_mode: 2bits>
            # Note: deep_dis = 0 (enable Deep_sleep mode), deep_dis = 1 (disable Deep_sleep mode)
            self.write_register(BMP581_ODR_REG, 0b10000001)  # Set output data rate
            print("BMP581 initialized successfully.")
            return None

        except Exception as e:
            print(f"Error initializing BMP581: {e}")
            return None

    def write_register(self, register, data):
        """Write data to a specific register."""
        bus.write_byte_data(BMP581_I2C_ADDRESS, register, data)
        return None

    def read_register(self, register, length):
        """Read data from a specific register."""
        return bus.read_i2c_block_data(BMP581_I2C_ADDRESS, register, length)

    def read_sensor_data(self):
        """Read pressure and temperature data from the BMP581 sensor."""
        try:
            # Read pressure data (replace with actual register and length)
            pressure_data = self.read_register(BMP581_PRESSURE_REG, 3)
            pressure = (pressure_data[2] << 16) | (pressure_data[1] << 8) | (pressure_data[0])
            pressure = pressure / 2**6  # Convert to meaningful units (check datasheet)
            print(f"Pressure data: {pressure_data}")

            # Read temperature data (replace with actual register and length)
            temp_data = self.read_register(BMP581_TEMPERATURE_REG, 3)
            temperature = (temp_data[2] << 16) | (temp_data[1] << 8) | (temp_data[0])
            temperature = temperature / 2**16  # Convert to meaningful units (check datasheet)
            print(f"Temperature data: {temp_data}")

            return pressure, temperature
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            return None, None