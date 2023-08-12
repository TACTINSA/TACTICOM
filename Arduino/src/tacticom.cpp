#include <Arduino.h>
#include "tacticom.h"

Tacticom::Tacticom(const String &prefix, void (*commands_handler)(const String &, const String *, uint8_t)) : prefix(prefix + "+"), commands_handler(commands_handler) {}

void Tacticom::tick() {
    if (Serial.available() <= 0) return; // No data available

    String raw = Serial.readStringUntil('\n');
    raw.trim();

    if (!raw.startsWith(prefix)) return; // Not a valid command

    String command = raw.substring(prefix.length());

    String command_name;
    String command_args;

    if (command.indexOf('=') == -1) {
        command_name = command;
        command_args = "";
    } else {
        command_name = command.substring(0, command.indexOf('='));
        command_args = command.substring(command.indexOf('=') + 1);
    }

    uint8_t args_count = 0;
    for (unsigned int i = 0; i < command_args.length(); i++) {
        if (command_args.charAt(i) == ',') args_count++;
    }

    String args[args_count + 1];

    uint8_t last_index = 0;
    uint8_t current_index = 0;
    for (unsigned int i = 0; i < command_args.length(); i++) {
        if (command_args.charAt(i) == ',') {
            args[current_index] = command_args.substring(last_index, i);
            last_index = i + 1;
            current_index++;
        }
    }

    args[current_index] = command_args.substring(last_index);

    commands_handler(command_name, args, args_count + 1);
}

void Tacticom::send(const String &name, const String *args, uint8_t args_count) {
    Serial.print(prefix);
    Serial.print(name);
    if (args_count > 0 && args != nullptr) {
        Serial.print('=');
        for (uint8_t i = 0; i < args_count; i++) {
            Serial.print(args[i]);
            if (i != args_count - 1) Serial.print(',');
        }
    }
    Serial.println();
}

void Tacticom::send(const String &name) {
    send(name, nullptr, 0);
}
