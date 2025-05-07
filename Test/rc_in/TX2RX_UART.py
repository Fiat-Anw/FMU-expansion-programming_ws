#!/usr/bin/python3
import time
import serial

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)

try:
    # Send a simple header
    serial_port.write("TX2RX_UART Testing Program\r\n".encode())
    serial_port.write("NVIDIA Jetson Orin Nano Developer Kit\r\n".encode())
    
    while True:
        # Send the desired message
        serial_port.write("Oh Hi!".encode())
        time.sleep(1)  # Add a delay to control the sending frequency

except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass