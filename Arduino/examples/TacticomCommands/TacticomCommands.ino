#include "tacticom.h"

// Prototype of the commands_handler function
void commands_handler(const String &name, const String &answer_code, const String &ask_code, const String *args,
                      uint8_t args_count);

// Initialize the Tacticom object with the prefix "R1" and the commands_handler function
TactiCom tc("R1", commands_handler);

void setup() {
    pinMode(LED_BUILTIN, OUTPUT); // Initialize the built-in LED as an output

    Serial.begin(115200); // Initialize the serial port
}

void loop() {
    tc.tick(); // Periodically check for new received commands
}

// Handle here all received commands
void commands_handler(const String &name, const String &answer_code, const String &ask_code, const String *args,
                      const uint8_t args_count) {
    // Debug print the received command
    Serial.print("name: " + name);
    Serial.print("\tanswer_code: " + answer_code);
    Serial.print("\task_code: " + ask_code);
    Serial.print("\targs_count: ");
    Serial.print(args_count);
    Serial.print("\targs: ");
    for (int i = 0; i < args_count; i++) {
        Serial.print(args[i]);
        Serial.print("|");
    }
    Serial.println();

    // Handle the received command
    if (name == "led") {
        if (args_count != 1) {
            // assert correct number of arguments
            const String error = "missing_args";
            tc.send_reply("led_error", ask_code, &error, 1);
            return;
        }
        digitalWrite(LED_BUILTIN, args[0] == "on" ? HIGH : LOW);
    } else if (name == "ping") {
        tc.send_reply("pong", ask_code); // reply pong
    } else if (name == "add") {
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
    } else if (name == "divide") {
        if (args_count != 2) {
            // assert correct number of arguments
            const String error = "missing_args";
            tc.send_reply("divide_error", ask_code, &error, 1);
            return;
        }

        const long a = args[0].toInt();
        const long b = args[1].toInt();

        if (b == 0) {
            const String error = "division_by_zero";
            tc.send_reply("divide_error", ask_code, &error, 1);
            return;
        }

        const auto result_divide = String(a / b); // division
        const auto result_modulo = String(a % b); // modulo
        tc.send_reply("divide_result", ask_code, new String[2]{result_divide, result_modulo}, 2); // reply with the result
    } else {
        const String error = "unknown_command";
        tc.send_reply("error", ask_code, &error, 1);
    }
}
