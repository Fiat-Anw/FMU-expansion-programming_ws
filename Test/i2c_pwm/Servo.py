# SDA = pin.SDA_1
# SCL = pin.SCL_1
# SDA_1 = pin.SDA
# SCL_1 = pin.SCL

import Jetson.GPIO as GPIO
from adafruit_servokit import ServoKit
import board
from busio import I2C
import time

R_LED_PIN = 7  # Change this to the GPIO number you're using
G_LED_PIN = 11  # Change this to the GPIO number you're using
B_LED_PIN = 15  # Change this to the GPIO number you're using

# Clean the previous GPIO settings to avoid conflicts
GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
# Set pin as output and set initial state
GPIO.setup(R_LED_PIN, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(G_LED_PIN, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(B_LED_PIN, GPIO.OUT, initial= GPIO.LOW)

# On the Jetson Nano
# Bus 0 (pins 28,27) is board SCL_1, SDA_1 in the jetson board definition file
# Bus 1 (pins 5, 3) is board SCL, SDA in the jetson definition file
# Default is to Bus 1; We are using Bus 0, so we need to construct the busio first ...
print("Initializing Servos")
## uncomment the next line to use Bus 0
# i2c_bus = (I2C(board.SCL_1, board.SDA_1))  #  I2C bus 0
i2c_bus = board.I2C() # I2C bus 1

# Initialize ServoKit with external clock at 24.5765 MHz and 50 Hz PWM frequency
kit = ServoKit(
    channels=16,
    i2c=i2c_bus,                  # Select I2C Bus
    reference_clock_speed=24576500,  # External clock frequency in Hz
    frequency=50,                   # Desired PWM frequency in Hz
    use_external_clock=True          # Enable external clock
)
print("ServoKit initialized with external clock at 24.5765 MHz and 50 Hz PWM frequency.")

# kit[0] is the bottom servo
# kit[1] is the top servo
print("Done initializing")
try:
    while True:
        # Show ACT LED as BLUE when servo is done sweeping
        GPIO.output(R_LED_PIN, GPIO.LOW)
        GPIO.output(G_LED_PIN, GPIO.LOW)
        GPIO.output(B_LED_PIN, GPIO.HIGH)
        print("Going to 180")
        sweep = range(0,180)
        # Show ACT LED as Yellow when servo is sweeping
        GPIO.output(R_LED_PIN, GPIO.HIGH)
        GPIO.output(G_LED_PIN, GPIO.HIGH)
        for degree in sweep :
            for i in range(16):
                kit.servo[i].angle=degree
                time.sleep(0.1)
        # Show ACT LED as BLUE when servo is done sweeping
        GPIO.output(R_LED_PIN, GPIO.LOW)
        GPIO.output(G_LED_PIN, GPIO.LOW)
        GPIO.output(B_LED_PIN, GPIO.HIGH)
        time.sleep(0.5)

        print("Going back to 0")
        sweep = range(180,0, -1)
        # Show ACT LED as Yellow when servo is sweeping
        GPIO.output(R_LED_PIN, GPIO.HIGH)
        GPIO.output(G_LED_PIN, GPIO.HIGH)
        for degree in sweep :
            for i in range(16):
                kit.servo[i].angle=degree
                time.sleep(0.1)
        print("Done sweeping")

except KeyboardInterrupt:
    # Turn off all LEDs
    GPIO.output(R_LED_PIN, GPIO.LOW)
    GPIO.output(G_LED_PIN, GPIO.LOW)
    GPIO.output(B_LED_PIN, GPIO.LOW)

    # Servo go back to 0
    for i in range(16):
        kit.servo[i].angle=0