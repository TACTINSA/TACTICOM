"""
This example shows how to use the SerialTactiCom class to communicate with a TactiCom device using events and requests.
"""

import time

from tacticom import SerialTactiCom


def main():
    # Create a SerialTactiCom
    stc = SerialTactiCom("R1", "/dev/ttyUSB0", 115200)
    stc.open()  # Open the serial port
    print("Connected to TactiCom device")

    time.sleep(2)  # Let Arduino time to boot (Arduino resets on serial connection)

    # send an event
    stc.send_event("led", "on")

    # send a request
    print(stc.send_request("ping"))

    # send a request
    result_command, result_parameter = stc.send_request("add", "1", "2")
    print("The result is: " + result_parameter[0])

    # send a request
    result_command, result_parameter = stc.send_request("divide", "11", "5")
    if result_command == "divide_error":
        print("Error: " + result_parameter[0])
    else:
        print("The result is: " + result_parameter[0] + " r: " + result_parameter[1])

    stc.send_event("led", "off")

    input("Press Enter to exit...")

    # Close the communication port
    stc.close()


if __name__ == '__main__':
    main()
