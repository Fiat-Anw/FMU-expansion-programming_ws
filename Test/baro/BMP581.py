import smbus2
import time

# I2C address of the BMP581 sensor
BMP581_I2C_ADDRESS = 0x47  # Replace with your sensor's address if different

# Registers (replace with actual BMP581 register addresses from the datasheet)
BMP581_CHIP_ID_REG = 0x50       # Example: Chip ID register
BMP581_PRESSURE_REG = 0x20      # Example: Pressure data register
BMP581_TEMPERATURE_REG = 0x1D   # Example: Temperature data register

# Initialize the I2C bus
bus = smbus2.SMBus(1)  # Use I2C bus 1 (check your hardware setup)

def read_register(register, length):
    """Read data from a specific register."""
    return bus.read_i2c_block_data(BMP581_I2C_ADDRESS, register, length)

def read_sensor_data():
    """Read pressure and temperature data from the BMP581 sensor."""
    try:
        # Read pressure data (replace with actual register and length)
        pressure_data = read_register(BMP581_PRESSURE_REG, 3)
        pressure = (pressure_data[2] << 16) | (pressure_data[1] << 8) | (pressure_data[0])
        pressure = pressure / 2**6  # Convert to meaningful units (check datasheet)
        print(f"Pressure data: {pressure_data}")

        # Read temperature data (replace with actual register and length)
        temp_data = read_register(BMP581_TEMPERATURE_REG, 3)
        temperature = (temp_data[2] << 16) | (temp_data[1] << 8) | (temp_data[0])
        temperature = temperature / 2**16  # Convert to meaningful units (check datasheet)
        print(f"Temperature data: {temp_data}")

        return pressure, temperature
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None, None

try:
    while True:
        pressure, temperature = read_sensor_data()
        if pressure is not None and temperature is not None:
            print(f"Pressure: {pressure} Pa, Temperature: {temperature} °C")
        time.sleep(1)  # Delay between readings

except KeyboardInterrupt:
    print("Exiting...")
