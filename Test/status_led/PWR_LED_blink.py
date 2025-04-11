# This script for testing blinks an LED connected to a GPIO pin on a Jetson Orin Nano board.
# It uses the Jetson.GPIO library to control the GPIO pins.

import Jetson.GPIO as GPIO
import time

PWR_LED_PIN = 38  # Change this to the GPIO number you're using

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
# Set pin as output and set initial state
GPIO.setup(PWR_LED_PIN, GPIO.OUT, initial= GPIO.LOW)

try:
    while True:
        GPIO.output(PWR_LED_PIN, GPIO.HIGH)
        print("PWR LED ON")
        time.sleep(1)
        GPIO.output(PWR_LED_PIN, GPIO.LOW)
        print("PWR LED OFF")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.output(PWR_LED_PIN, GPIO.LOW)


# finally:
#     # Clean up GPIO settings
#     GPIO.cleanup()
#     GPIO.cleanup()
#     print("GPIO cleanup done")
