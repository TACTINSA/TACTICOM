#ifndef TACTICOM_TACTICOM_H
#define TACTICOM_TACTICOM_H
#include <Arduino.h>

class Tacticom {
private:
    void (*router)(const String &, const String *, uint8_t);
    String prefix;

public:
    Tacticom(void (*router)(const String &name, const String args[], uint8_t args_count), String prefix);
    void tick();
    void send(const String &name);
    void send(const String &name, const String args[], uint8_t args_count);
};

#endif //TACTICOM_TACTICOM_H
