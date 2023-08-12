import time

from src.tacticom import TactiCom


def commands_handler(command: str, arguments: list):
    print("Received command " + command + " with args: " + str(arguments))


tacticom = TactiCom("R1", "COM4", 115200, commands_handler)
tacticom.open()
print("Connected to TactiCom device")
while True:
    command_name = input("Enter command name: ")
    if command_name == "exit":
        break

    args = []
    while True:
        arg = input("Enter command args: ")
        if arg == "":
            break
        args.append(arg)

    tacticom.send(command_name, *args)

    time.sleep(0.5)  # Wait for device response before prompting for next command

tacticom.close()
