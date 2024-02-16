#include "tacticom.h"

TactiCom::TactiCom(const String &prefix,
                   void (*commands_handler)(
                       const String &name,
                       const String &answer_code,
                       const String &ask_code,
                       const String *args,
                       uint8_t args_count
                   ))
    : prefix(prefix + "+"),
      commands_handler(commands_handler) {
}

void TactiCom::tick() const {
    if (Serial.available() <= 0) return; // No new command available

    String raw = Serial.readStringUntil('\n');
    raw.trim();

    if (!raw.startsWith(prefix)) return; // Not a valid command


    // Parse the command
    unsigned int index = prefix.length();

    String command_answer_code;
    String command_ask_code;
    String command_args;

    if (raw[index] == '[') {
        command_answer_code = raw.substring(index + 1, raw.indexOf(']'));
        index += command_answer_code.length() + 2;
    }

    int ask_code_index = raw.indexOf('[', index);
    int args_index = raw.indexOf('=', index);

    String command_name = raw.substring(index, ask_code_index != -1
                                                   ? ask_code_index
                                                   : args_index != -1
                                                         ? args_index
                                                         : raw.length());

    if (ask_code_index != -1) {
        command_ask_code = raw.substring(ask_code_index + 1, args_index != -1 ? args_index - 1 : raw.length() - 1);
    }

    uint8_t args_count = 0;

    if (args_index != -1) {
        command_args = raw.substring(args_index + 1);
        args_count = 1;
    } else {
        command_args = "";
    }

    for (unsigned int i = 0; i < command_args.length(); i++) {
        if (command_args.charAt(i) == ',') args_count++;
    }

    String args[args_count];

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

    // Call the command handler
    commands_handler(command_name, command_answer_code, command_ask_code, args, args_count);
}

void TactiCom::send(const String &name, const String &answer_code, const String &ask_code, const String *args,
                    const uint8_t args_count) const {
    Serial.print(prefix);
    if (answer_code != "") {
        Serial.print('[');
        Serial.print(answer_code);
        Serial.print(']');
    }
    Serial.print(name);
    if (ask_code != "") {
        Serial.print('[');
        Serial.print(ask_code);
        Serial.print(']');
    }
    if (args_count > 0 && args != nullptr) {
        Serial.print('=');
        for (uint8_t i = 0; i < args_count; i++) {
            Serial.print(args[i]);
            if (i != args_count - 1) Serial.print(',');
        }
    }
    Serial.println();
}

void TactiCom::send_event(const String &name) const {
    send_event(name, nullptr, 0);
}

void TactiCom::send_event(const String &name, const String *args, const uint8_t args_count) const {
    send(name, "", "", args, args_count);
}

void TactiCom::send_request(const String &name, const String &ask_code) const {
    send_request(name, ask_code, nullptr, 0);
}

void TactiCom::send_request(const String &name, const String &ask_code, const String *args, const uint8_t args_count) const {
    send(name, "", ask_code, args, args_count);
}

void TactiCom::send_reply(const String &name, const String &answer_code) const {
    send_reply(name, answer_code, nullptr, 0);
}

void TactiCom::send_reply(const String &name, const String &answer_code, const String *args, const uint8_t args_count) const {
    send(name, answer_code, "", args, args_count);
}