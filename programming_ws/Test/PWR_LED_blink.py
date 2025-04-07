# This script for testing blinks an LED connected to a GPIO pin on a Jetson Orin Nano board.
# It uses the Jetson.GPIO library to control the GPIO pins.

import Jetson.GPIO as GPIO
import time

R_LED_PIN = 7  # Change this to the GPIO number you're using
G_LED_PIN = 11  # Change this to the GPIO number you're using
B_LED_PIN = 15  # Change this to the GPIO number you're using

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
# Set pin as output and turn on i initial state
GPIO.setup(R_LED_PIN, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(G_LED_PIN, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(B_LED_PIN, GPIO.OUT, initial= GPIO.LOW)

try:
    while True:
        print("Red LED ON")
        GPIO.output(R_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(R_LED_PIN, GPIO.LOW)
        print("Green LED ON")
        GPIO.output(G_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        print("Blue LED ON")
        GPIO.output(G_LED_PIN, GPIO.LOW)    # Turn off Green LED
        GPIO.output(B_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        print("Red and Green LEDs ON")
        GPIO.output(B_LED_PIN, GPIO.LOW)    # Turn off Blue LED
        GPIO.output(R_LED_PIN, GPIO.HIGH)
        GPIO.output(G_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        print("Red and Blue LEDs ON")
        GPIO.output(G_LED_PIN, GPIO.LOW)    # Turn off Green LED
        GPIO.output(B_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        print("Green and Blue LEDs ON")
        GPIO.output(R_LED_PIN, GPIO.LOW)    # Turn off Red LED
        GPIO.output(G_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        print("All LEDs ON")
        GPIO.output(R_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        print("All LEDs OFF")
        GPIO.output(R_LED_PIN, GPIO.LOW)
        GPIO.output(B_LED_PIN, GPIO.LOW)
        GPIO.output(G_LED_PIN, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
