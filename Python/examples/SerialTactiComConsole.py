"""
This is a simple console application to send commands to a TactiCom device through serial and print the responses.
The example use TactiSerial but can be easily adapted to use another TactiCom implementation.
"""
import asyncio
import time

from tacticom import SerialTactiCom


def commands_handler(command: str, ask_code: str, reply_code: str, arguments: list):
    """Function to handle received commands"""
    print("Received command " + command + " with args: " + str(arguments))


# Create a SerialTactiCom. Can be replaced by another TactiCom implementation. Here we ignore invalid messages to allow
# the arduino to send raw debug serial messages
stc = SerialTactiCom("R1", "/dev/ttyACM0", 115200, commands_handler, on_invalid_message="ignore")
stc.open()  # Open the serial port

print("Connected to TactiCom device")
while True:
    # Prompt for command name
    command_name = input("Enter command name: ")
    if command_name == "exit":
        break

    # Prompt for command type
    while True:
        command_type = input("Should this command be sent as an event or a request? (event/request): ")
        if command_type in ["e", "event"]:
            is_request = False
            break
        elif command_type in ["r", "request"]:
            is_request = True
            break

        print("Invalid command type")

    # Prompt for command args
    args = []
    while True:
        arg = input("Enter command args (add empty argument to finish): ")
        if arg == "":
            break
        args.append(arg)

    # Send the command
    if is_request:
        try:
            # We don't care about the result as we don't use a CommandRegister
            asyncio.run(stc.send_request(command_name, *args, wait=False))
        except TimeoutError:
            print("Timeout waiting for reply")
    else:
        stc.send_event(command_name, *args)

    time.sleep(0.5)  # Wait for device response before prompting for next command

stc.close()  # Close the communication port
