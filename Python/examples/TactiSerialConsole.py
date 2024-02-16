"""
This example demonstrates how to use TactiSerial to communicate with a device through a serial port.
Here, TactiCom protocol is not used! TactiSerial provides async communication with a device through a serial port.
For combination with TactiCom, see SerialTactiComExample.py.
"""

from tacticom import TactiSerial


def on_message(message: str):
    """Function to be called when a message is received"""
    print(message)


# Create a TactiSerial
ts = TactiSerial("COM4", 115200, on_message)
ts.open()  # Open the serial port

print("Connected to device")
while True:
    inp = input()  # Wait for user input
    if inp == "exit":  # Exit if the user types "exit"
        break

    ts.send(inp)  # Send the user input to the device

ts.close()
