import serial

# SBUS constants
SBUS_FRAME_LEN = 25
SBUS_CHANNELS = 16
SBUS_HEADER = 0x0F
SBUS_END = 0x00

def parse_sbus_frame(frame):
    """Parse SBUS frame and extract channel values."""
    channels = []
    if len(frame) != SBUS_FRAME_LEN:
        return None

    # Extract 16 channels (11 bits each) from the SBUS frame
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
    channels.append((frame[14] >> 6 | frame[15] << 2 | frame[16] << 10) & 0x07FF)
    channels.append((frame[16] >> 1 | frame[17] << 7) & 0x07FF)
    channels.append((frame[17] >> 4 | frame[18] << 4) & 0x07FF)
    channels.append((frame[18] >> 7 | frame[19] << 1 | frame[20] << 9) & 0x07FF)
    channels.append((frame[20] >> 2 | frame[21] << 6) & 0x07FF)
    channels.append((frame[21] >> 5 | frame[22] << 3) & 0x07FF)

    return channels

def main():
    # Configure the serial port
    serial_port = '/dev/ttyTHS1'  # Replace with your UART port
    baud_rate = 100000  # SBUS baud rate
    timeout = 0.02  # 20ms timeout

    try:
        with serial.Serial(serial_port, baud_rate, timeout=timeout) as ser:
            print("Listening for SBUS data...")
            while True:
                # Read a frame
                data = ser.read(SBUS_FRAME_LEN)
                if len(data) == SBUS_FRAME_LEN and data[0] == SBUS_HEADER and data[-1] == SBUS_END:
                    channels = parse_sbus_frame(data)
                    if channels:
                        print("Channel values:", channels)
                else:
                    print("Invalid SBUS frame received.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()