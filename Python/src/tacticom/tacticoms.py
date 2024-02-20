import threading
from abc import ABC, abstractmethod
from typing import Callable, Any, TextIO
from uuid import uuid4

from tacticom.tactiprotocol import TactiMessage, parse_tactimessage


class CommandRegister:
    events_handlers: dict[str, Callable[..., Any]] = {}
    request_handlers: dict[str, Callable[..., Any]] = {}

    def on_event(self, event: str, handler: Callable[..., Any]) -> None:
        """
        Register an event handler

        :param event: name of the event
        :param handler: the handler to call when the event is received
        """
        self.events_handlers[event] = handler

    def on_request(self, request: str, handler: Callable[..., Any]) -> None:
        """
        Register a request handler

        :param request: name of the request
        :param handler: the handler to call when the request is received
        """
        self.request_handlers[request] = handler

    def __call__(self, command: str, ask_code: str, answer_code: str, arguments: list):
        if command in self.request_handlers:
            return self.request_handlers[command](*arguments)
        elif command in self.events_handlers:
            self.events_handlers[command](*arguments)
            return None
        else:
            raise ValueError(f"Invalid command: {command}")


class TactiCom(ABC):
    """TactiCom is the base class for all TactiCom implementations

    :param prefix: The prefix to use. Must be the same on each side.
    :param commands_handler: A command register (recommended) or a callable that handle when command are received. If a callable is used, it must return a tuple of the form (command, *args) if a reply is expected, or None if no reply is expected.
    :param on_invalid_message: What to do when an invalid message is received. Can be:
        - "raise": raise a ValueError
        - "ignore": ignore the message
        - a callable that will be called with the invalid message as argument
    :param timeout: The timeout in seconds to use when waiting for a reply
    """

    def __init__(self, prefix: str,
                 commands_handler: Callable[[str, str, str, list], Any] | CommandRegister,
                 on_invalid_message: str | Callable[[str], None] = "raise",
                 timeout: float = 5):
        self.prefix = prefix
        self.commands_handler = commands_handler
        self.on_invalid_message = on_invalid_message
        self.timeout = timeout

        self._waiting_replies: dict[str, threading.Event] = {}  # Dictionary of events waiting for a reply
        self._received_replies = {}  # Dictionary of received replies of requests

    def _on_message(self, message_str: str) -> None:
        """Handle a message received from the other side. Must be called by subclasses when a message is received."""
        try:
            message = parse_tactimessage(message_str)

            if message.prefix != self.prefix:
                raise ValueError(f"Invalid prefix: {message.prefix} (expected: {self.prefix})")
        except ValueError as e:
            # Handle invalid message
            match self.on_invalid_message:
                case "raise":  # propagate the exception
                    raise e
                case "ignore":  # ignore the message
                    return
                case _:  # call the custom handler
                    self.on_invalid_message(message_str)
                    return

        if (message.answer_code in self._waiting_replies
                and isinstance(self.commands_handler, CommandRegister)):  # If the message is a reply
            self._waiting_replies.pop(message.answer_code).set()
            self._received_replies[message.answer_code] = message.command, message.arguments
        else:  # If the message is an event or a request
            result = self.commands_handler(message.command, message.ask_code, message.answer_code, message.arguments)
            if result is not None:
                self.send_reply(message.ask_code, result[0], *result[1:])

    def send_event(self, message: str, *args) -> None:
        """Send an event to the other side, without waiting for a reply"""
        self._send_message(TactiMessage(self.prefix, None, message, None, list(args)))

    def send_request(self, message: str, *args, wait=True) -> tuple[str, list]:
        """
        Send a reply request to the other side and wait for the reply (if wait is True).

        :param message: The message to send
        :param args: The arguments to send
        :param wait: If False, return immediately after sending the request
        :return: The reply as a tuple of the form (command, *args)
        :raises TimeoutError: If no reply is received in time
        """
        guid = str(uuid4())  # Generate a unique identifier for the request
        event = threading.Event()
        self._waiting_replies[guid] = event
        self._send_message(TactiMessage(self.prefix, None, message, guid, list(args)))

        if not wait:  # If we don't want to wait for the reply, return immediately
            return "", []

        if not event.wait(self.timeout):  # Wait for the reply
            raise TimeoutError("Timeout waiting for reply")

        return self._received_replies.pop(guid)  # Return the received reply and remove it from the list

    def send_reply(self, answer_code: str, message: str, *args) -> None:
        """Send a reply to the other side to answer a request"""
        self._send_message(TactiMessage(self.prefix, answer_code, message, None, list(args)))

    def get_command_register(self) -> CommandRegister:
        if isinstance(self.commands_handler, CommandRegister):
            return self.commands_handler
        else:
            raise ValueError("The commands_handler is not a CommandRegister")

    @abstractmethod
    def _send_message(self, message: TactiMessage) -> None:
        """Send a message to the other side. Must be implemented by subclasses"""
        pass


class SerialTactiCom(TactiCom):
    """TactiCom implementation for serial communication through TactiSerial

    :param prefix: The prefix to use. Must be the same on each side.
    :param port: The serial port to use
    :param baudrate: The baudrate to use
    :param commands_handler: A command register (recommended) or a callable that handle when command are received. If a
        callable is used, it must return a tuple of the form (command, *args) if a reply is expected, or None if no
        reply is expected.
    :param on_invalid_message: What to do when an invalid message is received. Can be:
        - "raise": raise a ValueError
        - "ignore": ignore the message
        - a callable that will be called with the invalid message as argument
    :param timeout: The timeout in seconds to use when waiting for a reply
    :param poll_sleep_time: The time in seconds to wait between each poll of the serial port
    """

    def __init__(self, prefix: str,
                 port: str,
                 baudrate: int,
                 commands_handler: Callable[[str, str, str, list], Any] | CommandRegister = CommandRegister(),
                 on_invalid_message: str | Callable[[str], None] = "raise",
                 timeout: float = 5,
                 poll_sleep_time: float = 0.1):
        super().__init__(prefix, commands_handler, on_invalid_message, timeout)

        from tacticom import TactiSerial
        self._ts = TactiSerial(port, baudrate, self._on_message, poll_sleep_time=poll_sleep_time)

    def _send_message(self, message: TactiMessage) -> None:
        self._ts.send(str(message))

    def open(self) -> None:
        """Open the serial port"""
        self._ts.open()

    def close(self) -> None:
        """Close the serial port"""
        self._ts.close()


class TextIOTactiCom(TactiCom):
    """TactiCom implementation for TextIO streams & subprocesses communication

    :param prefix: The prefix to use. Must be the same on each side.
    :param command_input: The input stream to use to read commands
    :param command_output: The output stream to use to write commands
    :param commands_handler: A command register (recommended) or a callable that handle when command are received. If a
        callable is used, it must return a tuple of the form (command, *args) if a reply is expected, or None if no
        reply is expected.
    :param on_invalid_message: What to do when an invalid message is received. Can be:
        - "raise": raise a ValueError
        - "ignore": ignore the message
        - a callable that will be called with the invalid message as argument
    :param timeout: The timeout in seconds to use when waiting for a reply
    """

    def __init__(self, prefix: str,
                 command_input: TextIO,
                 command_output: TextIO,
                 commands_handler: Callable[[str, str, str, list], Any] | CommandRegister = CommandRegister(),
                 on_invalid_message: str | Callable[[str], None] = "raise",
                 timeout: float = 5):
        super().__init__(prefix, commands_handler, on_invalid_message, timeout)
        self.command_input = command_input
        self.command_output = command_output

        self._poll_message_thread = threading.Thread(target=self._poll_message)
        self._poll_message_thread.daemon = True
        self._poll_message_thread.start()

    def _send_message(self, message: TactiMessage) -> None:
        print(message, file=self.command_output)

    def _poll_message(self):
        while True:
            message = self.command_input.readline().strip()
            if message:
                self._on_message(message)

