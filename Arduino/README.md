# TACTICOM - Arduino library

## Installation
#### Using PlatformIO (recommended)
Add this repository (`https://github.com/TACTINSA/TACTICOM.git`) as a `lib_deps` in `platformio.ini`. Eg:
```ini
# platformio.ini
[env:uno]
platform = atmelavr
board = uno
framework = arduino
lib_deps = 
	https://github.com/TACTINSA/TACTICOM.git
```

#### Using Arduino IDE
Download Arduino folder as ZIP: [Download link](https://minhaskamal.github.io/DownGit/#/home?url=https:%2F%2Fgithub.com%2FTACTINSA%2FTACTICOM%2Ftree%2Fmaster%2FArduino&fileName=tacticom_arduino)
In Arduino IDE, under `Sketch` -> `Include Library` -> `Add .ZIP Library...` select the downloaded file. 

## Usage
1. Include the library
```cpp
// Begining of the file
#include "tacticom.h"
```
2. Initialisation
```cpp
// Before setup function
void commands_handler(const String &name, const String args[], uint8_t args_count); // Prototype for the function handling recieved commands
Tacticom tacticom("R1", commands_handler); // Init Tacticom with a prefix and the handling function 

...

// In setup function
void setup() {
    Serial.begin(115200); // Start the serial communication
}

...

// In loop function
void loop() {
    tacticom.tick(); // Periodicaly check for new received commands
}
```

2. Sending commands to USB Device/Raspberry:
```cpp
tacticom.send("pong"); // Without arguments
tacticom.send("add_result", &s, 1); // With one argument (s being a String, 1 being the number of arguments)
tacticom.send("divide_result", new String[2]{s1, s2}, 2); // With multiple arguments (s1 & s2 being String, 2 being the number of arguments)
```
3. Receiving commands
```cpp
void commands_handler(const String &name, const String *args, uint8_t args_count) { // Handle here all received commands
    if (name == "ping") {
        tacticom.send("pong"); // reply pong
    } else if (name == "add") {
        if (args_count != 2) return; // assert correct number of arguments

        String s = String(args[0].toInt() + args[1].toInt()); // Add the two parameters
        tacticom.send("add_result", &s, 1); // reply with the result
    } else if (name == "divide") {
        if (args_count != 2) return; // assert correct number of arguments

        long a = args[0].toInt();
        long b = args[1].toInt();
        String s1 = String(a / b); // division
        String s2 = String(a % b); // modulo
        tacticom.send("divide_result", new String[2]{s1, s2}, 2); // reply with the result
    }
}
```

## Examples
+ [Sample usage of TactiCom](examples/TacticomCommands/TacticomCommands.ino)
