#ifndef TACTICOM_TACTICOM_H
#define TACTICOM_TACTICOM_H

#include <Arduino.h>

class Tacticom {
private:
    String prefix;

    void (*commands_handler)(const String &name, const String &answer_code, const String &ask_code, const String *args, uint8_t args_count);

public:
    Tacticom(const String &prefix, void (*commands_handler)(const String &name, const String &answer_code, const String &ask_code, const String *args, uint8_t args_count));

    void tick();

    void send(const String &name, const String &answer_code, const String *args, uint8_t args_count);

    void send_message(const String &name);

    void send_message(const String &name, const String *args, uint8_t args_count);

    void answer_message(const String &name, const String &answer_code);

    void answer_message(const String &name, const String &answer_code, const String *args, uint8_t args_count);
};

#endif //TACTICOM_TACTICOM_H
