import time

from src.tacticom import TactiCom


def commands_handler(command: str, arguments: list):
    match command:
        case "pong":
            print("Received pong")
        case "add_result":
            print("Received add_result with args: " + str(arguments))
        case "divide_result":
            print("Received divide_result with args: " + str(arguments))


tacticom = TactiCom("R1", "COM4", 115200, commands_handler)
tacticom.open()
print("Connected to TactiCom device")
time.sleep(2)  # Let Arduino time to boot (Arduino resets on serial connection)
tacticom.send("ping")
tacticom.send("add", "1", "2")
tacticom.send("divide", "1", "2")

while True:
    if input() == "exit":
        break

tacticom.close()
