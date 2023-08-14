#ifndef TACTICOM_TACTICOM_H
#define TACTICOM_TACTICOM_H
#include <Arduino.h>

class Tacticom {
private:
    String prefix;
    void (*commands_handler)(const String &, const String *, uint8_t);

public:
    Tacticom(const String& prefix, void (*commands_handler)(const String &name, const String args[], uint8_t args_count));
    void tick();
    void send(const String &name);
    void send(const String &name, const String args[], uint8_t args_count);
};

#endif //TACTICOM_TACTICOM_H
