from src.tacticom import TactiSerial


def on_message(message: str):
    print(message)


tactiserial = TactiSerial("COM4", 115200, on_message)
tactiserial.open()
print("Connected to device")
while True:
    inp = input()
    if inp == "exit":
        break

    tactiserial.send(inp)

tactiserial.close()
