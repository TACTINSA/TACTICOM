#include "tacticom.h"


void commands_handler(const String &name, const String args[], uint8_t args_count);

Tacticom tacticom("R1", commands_handler); // Command will be "R1+command_name=arg1,arg2,arg3" (eg "R1+ping")

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

void setup() {
    Serial.begin(115200);
}

void loop() {
    tacticom.tick(); // Periodically check for new received commands
}