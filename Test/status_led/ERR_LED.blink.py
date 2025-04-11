# This script for testing blinks an LED connected to a GPIO pin on a Jetson Orin Nano board.
# It uses the Jetson.GPIO library to control the GPIO pins.

import Jetson.GPIO as GPIO
import time

ERR_LED_PIN = 40  # Change this to the GPIO number you're using

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
# Set pin as output and set initial state
GPIO.setup(ERR_LED_PIN, GPIO.OUT, initial= GPIO.LOW)

try:
    while True:
        GPIO.output(ERR_LED_PIN, GPIO.HIGH)
        print("ERR LED ON")
        time.sleep(1)
        GPIO.output(ERR_LED_PIN, GPIO.LOW)
        print("ERR LED OFF")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.output(ERR_LED_PIN, GPIO.LOW)


# finally:
#     # Clean up GPIO settings
#     GPIO.cleanup()
#     GPIO.cleanup()
#     print("GPIO cleanup done")
