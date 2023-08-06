#include <Arduino.h>
#include "tacticom.h"


void router(const String &name, const String args[], uint8_t args_count);

Tacticom tacticom(router, "R1"); // Command will be "R1+command_name=arg1,arg2,arg3" (eg "R1+ping")

void router(const String &name, const String *args, uint8_t args_count) { // declare here all commands
    if (name == "ping") {
        tacticom.send("pong"); // send back a message
    } else if (name == "test") {
        if (args_count != 3) return;

        String s = String(args[0].toInt() + args[1].toInt() + args[2].toInt());
        tacticom.send("test_response", &s, 1); // send back a message with one argument
    } else if (name == "test2") {
        if (args_count != 3) return;

        String s1 = String(args[0].toInt() + args[1].toInt());
        String s2 = String(args[1].toInt() + args[2].toInt());
        tacticom.send("test_response", new String[2]{s1, s2}, 2);
    }
}

void setup() {
    Serial.begin(115200);
}

void loop() {
    tacticom.tick();
}