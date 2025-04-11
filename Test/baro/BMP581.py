from BMP581_DRIVE import BMP581  # Import the BMP581 class from the BMP581_DRIVE
import time

try:
    sensor = BMP581()  # Initialize the sensor
    while True:
        pressure, temperature = sensor.read_sensor_data()
        if pressure is not None and temperature is not None:
            print(f"Pressure: {pressure} Pa, Temperature: {temperature} °C")
        time.sleep(1)  # Delay between readings

except KeyboardInterrupt:
    print("Exiting...")
