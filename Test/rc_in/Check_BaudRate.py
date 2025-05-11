import serial
import time

# UART port to test (change if needed)
UART_PORT = '/dev/ttyTHS1'

# SBUS characteristics
BAUD_RATES = [100000, 115200, 9600, 57600, 19200]  # Include 100000 for SBUS
EXPECTED_FRAME_LENGTH = 25
START_BYTE = 0x0F
END_BYTE = 0x00

def is_valid_sbus_frame(data):
    """ Validate SBUS frame based on length and start/end bytes """
    return len(data) == EXPECTED_FRAME_LENGTH and data[0] == START_BYTE and data[24] == END_BYTE

def detect_sbus_baud(port):
    for baud in BAUD_RATES:
        try:
            print(f"Testing baud rate: {baud}")
            with serial.Serial(port, baudrate=baud, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO, timeout=1) as ser:
                ser.reset_input_buffer()
                start_time = time.time()

                while time.time() - start_time < 3:  # Test for 3 seconds
                    data = ser.read(EXPECTED_FRAME_LENGTH)
                    if is_valid_sbus_frame(data):
                        print(f"\nDetected SBUS baud rate: {baud}")
                        print(f"SBUS Frame: {data.hex()}")
                        return baud

        except Exception as e:
            print(f"Error testing baud {baud}: {e}")

    print("\nNo valid SBUS baud rate found.")
    return None

if __name__ == "__main__":
    detected_baud = detect_sbus_baud(UART_PORT)
    if detected_baud:
        print(f"Detected working SBUS baud rate: {detected_baud}")
    else:
        print("SBUS baud rate detection failed.")