# TACTICOM
TACTINSA serial communication protocol for the French Robotic Cup robots \
\
This library provides easy to setup and reliable communication between two devices through a serial port. We mainly use it between RaspberryPi and Arduino through the Python and Arduino implementation.

## Communication protocol
Message are sent through command: `PREFIX+command_name=arg1,arg2`
+ PREFIX is a small string prefixing all messages. (eg: We use R1 for our first robot, R2 for the second, ...)
+ command_name is a string that identify the data being exchanged
+ args are transmitted encoded as string and separated by commas. If no arguments are exchanged, the = is omited 

## Implementation
### Python
[Documentation for Python library](Python/README.md)

### Arduino
[Documentation for Arduino library](Arduino/README.md)
