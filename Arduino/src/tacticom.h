#ifndef TACTICOM_TACTICOM_H
#define TACTICOM_TACTICOM_H

#include <Arduino.h>

class TactiCom {
    String prefix;

    void (*commands_handler)(const String &name,
                             const String &answer_code,
                             const String &ask_code,
                             const String *args,
                             uint8_t args_count);

public:
    /**
     * @brief Tacticom::Tacticom
     * @details Constructor for the Tacticom class.
     * @param prefix The prefix to be used for the commands. Must be the same as the one used in the connected device.
     * @param commands_handler The function that will be called when a command is received.
     */
    TactiCom(const String &prefix,
             void (*commands_handler)(const String &name,
                                      const String &answer_code,
                                      const String &ask_code,
                                      const String *args,
                                      uint8_t args_count)
    );

    /**
     * @brief Tacticom::tick
     * @details This method should be called in the loop function of the Arduino sketch.
     * It will read the serial port and call the commands_handler function when a valid command is received.
     */
    void tick() const;

    /**
     * @brief Tacticom::send
     * @details Send a command to the connected device through the serial port.
     */
    void send(const String &name, const String &answer_code, const String &ask_code, const String *args,
              uint8_t args_count) const;

    /**
     * @brief Tacticom::send_event
     * @details Send an event to the connected device through the serial port.
     */
    void send_event(const String &name) const;

    /**
     * @brief Tacticom::send_event
     * @details Send an event to the connected device through the serial port with arguments.
     */
    void send_event(const String &name, const String *args, uint8_t args_count) const;

    /**
     * @brief Tacticom::send_request
     * @details Send a request to the connected device through the serial port. Ask code must be an unique identifier
     * that will be provided back in the reply to identify it.
     */
    void send_request(const String &name, const String &ask_code) const;

    /**
     * @brief Tacticom::send_request
     * @details Send a reply to the connected device through the serial port with arguments. Ask code must be an unique
     * identifier that will be provided back in the reply to identify it.
     */
    void send_request(const String &name, const String &ask_code, const String *args, uint8_t args_count) const;

    /**
     * @brief Tacticom::send_reply
     * @details Send a reply to the connected device through the serial port. Answer code is the same as the one
     * received from the request.
     */
    void send_reply(const String &name, const String &answer_code) const;

    /**
     * @brief Tacticom::send_reply
     * @details Send a reply to the connected device through the serial port with arguments.
     */
    void send_reply(const String &name, const String &answer_code, const String *args, uint8_t args_count) const;
};

#endif //TACTICOM_TACTICOM_H
