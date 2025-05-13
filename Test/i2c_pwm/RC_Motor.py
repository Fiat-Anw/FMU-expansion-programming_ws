import Jetson.GPIO as GPIO
from adafruit_servokit import ServoKit
import board
from busio import I2C
import serial
import time

R_LED_PIN = 7  # Change this to the GPIO number you're using
G_LED_PIN = 11  # Change this to the GPIO number you're using
B_LED_PIN = 15  # Change this to the GPIO number you're using

# SBUS constants
SBUS_FRAME_LEN = 25
SBUS_CHANNELS = 10  # Updated to 10 channels
SBUS_HEADER = 0x0F
SBUS_END = 0x00

# Adjust the range as needed channels of I2C to PWM channels
I2CPWM_CHANNELS = [0, 1, 2]

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=100000,  # SBUS baud rate
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,  # Changed to even parity
    stopbits=serial.STOPBITS_TWO,  # Changed to 2 stopbits
)

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
print("ServoKit initialized with external clock at 24.5765 MHz PWM frequency.")
print("Done initializing")

def parse_sbus_frame(frame):
    """Parse SBUS frame and extract channel values."""
    channels = []
    if len(frame) != SBUS_FRAME_LEN:
        return None

    # Extract 10 channels (11 bits each) from the SBUS frame
    channels.append((frame[1] | frame[2] << 8) & 0x07FF)
    channels.append((frame[2] >> 3 | frame[3] << 5) & 0x07FF)
    channels.append((frame[3] >> 6 | frame[4] << 2 | frame[5] << 10) & 0x07FF)
    channels.append((frame[5] >> 1 | frame[6] << 7) & 0x07FF)
    channels.append((frame[6] >> 4 | frame[7] << 4) & 0x07FF)
    channels.append((frame[7] >> 7 | frame[8] << 1 | frame[9] << 9) & 0x07FF)
    channels.append((frame[9] >> 2 | frame[10] << 6) & 0x07FF)
    channels.append((frame[10] >> 5 | frame[11] << 3) & 0x07FF)
    channels.append((frame[12] | frame[13] << 8) & 0x07FF)
    channels.append((frame[13] >> 3 | frame[14] << 5) & 0x07FF)

    return channels

def map_value(value, in_min, in_max, out_min, out_max):
    """Map a value from one range to another."""
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def main():
    try:
        print("Listening for SBUS data...")
        while True:
            # Show ACT LED as BLUE when servo is done sweeping
            GPIO.output(R_LED_PIN, GPIO.LOW)
            GPIO.output(G_LED_PIN, GPIO.LOW)
            GPIO.output(B_LED_PIN, GPIO.HIGH)
            
            # Reset and Read data frame
            serial_port.reset_input_buffer()
            data = serial_port.read(SBUS_FRAME_LEN)
            if len(data) == SBUS_FRAME_LEN:
                print("Raw data:", " ".join(f"{byte:02X}" for byte in data))
                if data[0] == SBUS_HEADER and data[-1] == SBUS_END:
                    channels = parse_sbus_frame(data)
                    if channels:
                        print("Channel values:", channels)
                        # Show ACT LED as Yellow when servo is sweeping
                        GPIO.output(R_LED_PIN, GPIO.HIGH)
                        GPIO.output(G_LED_PIN, GPIO.HIGH)

                        # Adjust dead zone and calibration
                        dead_zone = 70
                        calibration_offset = 1042

                        for i in I2CPWM_CHANNELS:  # Adjust the range as needed channels
                            # Channels 1, 3 for left/right
                            # Channels 2 for forward/backward

                            # Special condition for DC motor which is channel 1 (forward/backward)
                            if i == 1:
                                # Check if the channel value is within the dead zone
                                # If it is, set the servo to a neutral position (102)
                                if (calibration_offset - dead_zone) <= channels[i] <= (calibration_offset + dead_zone):
                                    print(f"Channel {i} is within the dead zone, servo will not move.")
                                    angle = 102  # 102 is not moving
                                    kit.servo[i].angle = angle
                                    print(f"Setting servo {i} to angle: {angle} to stop")
                                    continue
                                # Calibrate channel 1 to have a center value of 1042
                                calibrated_value = channels[i] - calibration_offset
                                # Map the calibrated value to servo angle
                                angle = map_value(calibrated_value, -850, 750, 0, 180)
                            else:
                                # Map the channel value to servo angle for other channels
                                angle = map_value(channels[i], 192, 1792, 0, 180)

                            print(f"Setting servo {i} to angle: {angle}")
                            kit.servo[i].angle = angle
                    else:
                        print("Failed to parse channels.")
                else:
                    print("Invalid SBUS frame: Header or End byte mismatch.")
            else:
                print("Incomplete frame received.")
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Serial error: {e}")

    except KeyboardInterrupt:
        # Turn off all LEDs
        GPIO.output(R_LED_PIN, GPIO.LOW)
        GPIO.output(G_LED_PIN, GPIO.LOW)
        GPIO.output(B_LED_PIN, GPIO.LOW)
        print("Exiting...")

        # Servo go back to home position
        for i in I2CPWM_CHANNELS:

            # Special condition for DC motor which is channel 1 (forward/backward)
            if i == 1:
                kit.servo[i].angle=102  # 102 is not moving
                continue
            kit.servo[i].angle=90  # Set servo to neutral position (90 degrees)

    finally:
        serial_port.close()

if __name__ == "__main__":
    main()