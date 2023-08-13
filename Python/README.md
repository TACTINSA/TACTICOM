# TACTICOM - Python library

## Installation
Install through pip:
```bash
pip install -e "git+https://github.com/TACTINSA/TACTICOM/#egg=tacticom&subdirectory=Python"
```

## Usage
1. Initialisation
```py
arduino = TactiCom(PREFIX, PORT, BAUDRATE, commands_handler)
# Eg
arduino = TactiCom("R1", "/dev/arduino", 115200, commands_handler)
```
with commands_handler being the method handling received commands (see 3.)
2. Sending commands to Arduino:
```py
tacticom.send("ping") # Without arguments
tacticom.send("add", "1", "2") # With arguments
tacticom.send("divide", "1", "2") # With arguments
```
3. Recieving commands
```py
def commands_handler(command: str, arguments: list):
    match command:
        case "pong":
            print("Received pong")
        case "add_result":
            print("Result: " + arguments[0])
        case "divide_result":
            print("Result q: " + arguments[0] + " r: " + arguments[1])
```

## TactiSerial
TactiSerial is a threaded serial reader / writer behind TactiCom that can be used when the TactiCom communication protocol isn't required (Eg with a stock motor driver).

## Examples
+ [Sample usage of TactiCom](examples/TactiComExample.py)
+ [Console for playing with TactiCom](examples/TactiComConsole.py)
+ [Console for playing with TactiSerial](examples/TactiSerialConsole.py)
