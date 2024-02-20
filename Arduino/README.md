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
Download the Arduino library as a ZIP file [HERE](https://minhaskamal.github.io/DownGit/#/home?url=https:%2F%2Fgithub.com%2FTACTINSA%2FTACTICOM%2Ftree%2Fmaster%2FArduino&fileName=tacticom_arduino). \
In Arduino IDE, under `Sketch` -> `Include Library` -> `Add .ZIP Library...` select the downloaded file. 

## Usage
1. Include the library
```cpp
// Begining of the file
#include <tacticom.h>
```
2. Initialisation
```cpp
// Before setup function
void commands_handler(const String &name, const String &answer_code, const String &ask_code, const String *args, uint8_t args_count);
TactiCom tc("R1", commands_handler);
...

// In setup function
void setup() {
    Serial.begin(115200); // Start the serial communication
}

...

// In loop function
void loop() {
    tc.tick(); // Periodicaly check for new received commands
}
```

2. Sending commands to USB Device/Raspberry:
```cpp
tc.send_request("pong", "unique_identifier_for_this_request); // a request, without arguments
tc.send_event("led", &s, 1); // an event, with one argument (s being a String "on", 1 being the number of arguments)
tc.send_reply("divide_result", new String[2]{s1, s2}, 2); // a reply, with multiple arguments (s1 & s2 being String, 2 being the number of arguments)
```
3. Receiving commands
```cpp
void commands_handler(const String &name, const String &answer_code, const String &ask_code, const String *args,
                      const uint8_t args_count) {
                      
    if (name == "led") { // Handle an event
        if (args_count != 1) {
            // assert correct number of arguments
            const String error = "missing_args";
            tc.send_reply("led_error", ask_code, &error, 1);
            return;
        }
        digitalWrite(LED_BUILTIN, args[0] == "on" ? HIGH : LOW);
    } else if (name == "ping") { // Handle a request without arguments
        tc.send_reply("pong", ask_code); // reply pong
    } else if (name == "add") { // Handle a request with arguments
        if (args_count != 2) {
            // assert correct number of arguments
            const String error = "missing_args";
            tc.send_reply("add_error", ask_code, &error, 1);
            return;
        }
        const long a = args[0].toInt(); // convert the first parameter to a number
        const long b = args[1].toInt(); // convert the second parameter to a number
        const long result = a + b; // Calculate the sum
        const auto result_str = String(result); // Convert the result to a string
        tc.send_reply("add_result", ask_code, &result_str, 1); // reply with the result
    }
}

```

## Examples
+ [Sample usage of TactiCom on Arduino](examples/TacticomCommands/TacticomCommands.ino)
