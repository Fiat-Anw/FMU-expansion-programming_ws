import serial
import time

# SBUS constants
SBUS_FRAME_LEN = 25
SBUS_CHANNELS = 10  # Updated to 10 channels
SBUS_HEADER = 0x0F
SBUS_END = 0x00

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=100000,  # SBUS baud rate
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,  # Changed to even parity
    stopbits=serial.STOPBITS_TWO,  # Changed to 2 stopbits
)

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

def read_sbus_data(serial_port):
    buffer = bytearray()

    """Read and buffer SBUS data to handle incomplete or misaligned frames."""
    try:
        # Reset and Read a frame
        serial_port.reset_input_buffer()
        bytes = serial_port.read(SBUS_FRAME_LEN)
        if bytes:
            buffer.extend(bytes)

            # Check if the buffer contains a complete frame
            if len(buffer) >= SBUS_FRAME_LEN:
                print("Raw data:", " ".join(f"{byte:02X}" for byte in bytes))

                # Validate the frame
                if buffer[0] == SBUS_HEADER and buffer[SBUS_FRAME_LEN - 1] == SBUS_END:
                    frame = buffer[:SBUS_FRAME_LEN]
                    buffer = buffer[SBUS_FRAME_LEN:]  # Remove the processed frame
                    channels = parse_sbus_frame(frame)
                    if channels:
                        print("Channel values:", channels)
                    else:
                        print("Failed to parse channels.")
                else:
                    print("Invalid SBUS frame: Header or End byte mismatch.")
                    # Discard the first byte if the frame is invalid
                    buffer.pop(0)
                    
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return False
    return True

def main():
    try:
        print("Listening for SBUS data...")
        while True:
            if not read_sbus_data(serial_port):
                break

    except serial.SerialException as e:
        print(f"Serial error: {e}")

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        serial_port.close()

if __name__ == "__main__":
    main()