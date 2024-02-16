# TACTICOM - Python library

## Installation

Install through pip:

```bash
pip install -e "git+https://github.com/TACTINSA/TACTICOM/#egg=tacticom&subdirectory=Python"
```

## Usage

Multiple implementations of the TactiCom protocol are available:

+ Serial communication (e.g. with Arduino) -> `SerialTactiCom`
+ Subprocess communication (e.g. with another Python process) -> `SubprocessTactiCom`
  You can also use the Tacticom protocol through your own implementation by using the `TactiCom` class.

The following examples use the `SerialTactiCom` implementation, but code for the other implementations is similar (see
the `examples` folder).

1. Initialisation

```py
from tacticom import SerialTactiCom

stc = SerialTactiCom(PREFIX, PORT, BAUDRATE)
# Eg
stc = SerialTactiCom("R1", "/dev/ttyUSB0", 115200)

stc.open()  # Open the serial port
```

Prefix is of your choice, but it must be the same on both end of the communication.

2. Sending commands to the other end:

There is three types of messages:
- Event <=> A message that doesn't require an answer
- Request <=> A message that requires an answer
- Reply <=> An answer to a request

The name of the event/request/reply is called a command
 
To send one of these, use the `send_XXX` method:
```py
stc.send_event("led", "on")  # an event, with arguments
await stc.send_request("ping") # a request, without arguments
stc.send_reply("pong") # a reply, without arguments
stc.send_request("add", "1", "2")  # a request, with arguments
```

3. Recieving commands

To handle commands, the library provides a register. You can register a function to be called when a command is received.
```py
stc.get_command_register().on_request("add", lambda a, b: ("result", str(int(a) + int(b))))
stc.get_command_register().on_event("quit", lambda: exit())
```
You can also implement your own command handler that must be passed to the `SerialTactiCom`.
```py
def commands_handler(command: str, ask_code: str, reply_code: str, arguments: list):
    match command:
        case "pong":
            print("Received pong")
        case "add_result":
            print("Result: " + arguments[0])
        
stc = SerialTactiCom(..., commands_handler=commands_handler)
```

## TactiSerial

TactiSerial is a threaded serial reader / writer behind TactiCom that can be used when the TactiCom communication
protocol isn't required.

## Examples

+ [Sample usage of SerialTactiCom](examples/SerialTactiComExample.py)
+ [Sample usage of SubprocessTactiCom](examples/SubprocessTactiComExample.py)
+ [Console for playing with SerialTactiCom](examples/SerialTactiComConsole.py)
+ [Console for playing with TactiSerial (No TactiCom protocol)](examples/TactiSerialConsole.py)
