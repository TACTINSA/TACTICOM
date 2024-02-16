# TACTICOM
TACTINSA serial communication protocol for the French Robotic Cup robots \
\
This library provides easy and reliable communication between two devices through a serial port. We mainly use it between RaspberryPi and Arduino through the Python and Arduino implementation.

## Communication protocol
Message are sent through command: `PREFIX+[answer_code]command_name[ask_code]=arg1,arg2`
+ PREFIX is a small string prefixing all messages. (eg: We use R1 for our first robot, R2 for the second, ...)
+ answer_code is a string to identify the answer to a command. It is omitted if the message isn't a reply
+ command_name is a string that identify the data being exchanged
+ ask_code is a string to identify the command as a request for data. It is omitted if the message isn't a request
+ args are transmitted encoded as string and separated by commas. If no arguments are exchanged, the = is omitted

## Message types
Event <=> A message that doesn't require an answer \
Request <=> A message that requires an answer \
Reply <=> An answer to a request \
\
The name of the event/request/reply is called a command

## Implementation
### Python
[Documentation for Python library](Python/README.md)

### Arduino
[Documentation for Arduino library](Arduino/README.md)
