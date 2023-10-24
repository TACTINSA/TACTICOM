import threading
from abc import ABC, abstractmethod
from typing import Callable, Any, TextIO
from uuid import uuid4

from tacticom import tactiprotocol


class CommandRegister:
    event_commands: dict[str, Callable[[list], Any]] = {}
    reply_commands: dict[str, Callable[[list], Any]] = {}

    def register_event(self, command: str, handler: Callable[[list], Any]):
        self.event_commands[command] = handler

    def register_reply(self, command: str, handler: Callable[[list], Any]):
        self.reply_commands[command] = handler

    def __call__(self, command: str, ask_code: str, arguments: list):
        if ask_code is not None and command in self.reply_commands:
            return self.reply_commands[command](*arguments)
        elif ask_code is None and command in self.event_commands:
            self.event_commands[command](*arguments)
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

    def __init__(self, prefix: str, commands_handler: Callable[[str, str, list], Any] | CommandRegister, on_invalid_message: str | Callable[[str], None] = "raise", timeout: float = 5):
        self.prefix = prefix
        self.commands_handler = commands_handler
        self.on_invalid_message = on_invalid_message
        self.timeout = timeout

        self._in_waiting: dict[str, threading.Event] = {}
        self._results = {}

    def _on_message(self, message_str: str) -> None:
        try:
            message = tactiprotocol.parse(message_str)

            if message.prefix != self.prefix:
                raise ValueError(f"Invalid prefix: {message.prefix} (expected: {self.prefix})")
        except ValueError as e:
            if self.on_invalid_message == "raise":
                raise e
            elif self.on_invalid_message == "ignore":
                return
            else:
                self.on_invalid_message(message_str)
                return

        if message.answer_code in self._in_waiting:
            self._in_waiting.pop(message.answer_code).set()
            self._results[message.answer_code] = message.command, message.arguments
        else:
            result = self.commands_handler(message.command, message.ask_code, message.arguments)
            if message.ask_code is not None and result is not None:
                self.send_reply(message.ask_code, result[0], *result[1:])

    @abstractmethod
    def _send_message_to_other_side(self, message: str) -> None:
        """Send a message to the other side. Must be implemented by subclasses"""
        pass

    def _send_message(self, message: tactiprotocol.TactiMessage) -> None:
        """Send a TactiMessage to the other side"""
        self._send_message_to_other_side(tactiprotocol.serialize(message))

    def send_event(self, message: str, *args) -> None:
        """Send an event to the other side, without waiting for a reply"""
        self._send_message(tactiprotocol.TactiMessage(self.prefix, None, message, None, list(args)))

    async def send_request(self, message: str, *args) -> tuple[str, list]:
        """
        Send a reply request to the other side and wait for the reply.

        :return: The reply as a tuple of the form (command, *args)
        :raises TimeoutError: If no reply is received in time
        """
        guid = str(uuid4())
        event = threading.Event()
        self._in_waiting[guid] = event
        self._send_message(tactiprotocol.TactiMessage(self.prefix, None, message, guid, list(args)))
        if not event.wait(self.timeout):
            raise TimeoutError("Timeout waiting for reply")
        return self._results.pop(guid)

    def send_reply(self, answer_code: str, message: str, *args) -> None:
        """Send a reply to the other side for a previous request"""
        self._send_message(tactiprotocol.TactiMessage(self.prefix, answer_code, message, None, list(args)))


class SerialTactiCom(TactiCom):
    """TactiCom implementation for serial communication through TactiSerial

    :param prefix: The prefix to use. Must be the same on each side.
    :param port: The serial port to use
    :param baudrate: The baudrate to use
    :param commands_handler: A command register (recommended) or a callable that handle when command are received. If a callable is used, it must return a tuple of the form (command, *args) if a reply is expected, or None if no reply is expected.
    :param on_invalid_message: What to do when an invalid message is received. Can be:
        - "raise": raise a ValueError
        - "ignore": ignore the message
        - a callable that will be called with the invalid message as argument
    :param timeout: The timeout in seconds to use when waiting for a reply
    :param poll_sleep_time: The time in seconds to wait between each poll of the serial port
    """

    def __init__(self, prefix: str, port: str, baudrate: int, commands_handler: Callable[[str, str, list], Any] | CommandRegister, on_invalid_message: str | Callable[[str], None] = "raise", timeout: float = 5, poll_sleep_time: float = 0.1):
        super().__init__(prefix, commands_handler, on_invalid_message, timeout)

        from tacticom import TactiSerial
        self._ts = TactiSerial(port, baudrate, self._on_message, poll_sleep_time=poll_sleep_time)

    def _send_message_to_other_side(self, message: str) -> None:
        self._ts.send(message)

    def open(self) -> None:
        """Open the serial port"""
        self._ts.open()

    def close(self) -> None:
        """Close the serial port"""
        self._ts.close()


class SubprocessTactiCom(TactiCom):
    """TactiCom implementation for subprocesses communication

    :param prefix: The prefix to use. Must be the same on each side.
    :param command_input: The input stream to use to read commands
    :param command_output: The output stream to use to write commands
    :param commands_handler: A command register (recommended) or a callable that handle when command are received. If a callable is used, it must return a tuple of the form (command, *args) if a reply is expected, or None if no reply is expected.
    :param on_invalid_message: What to do when an invalid message is received. Can be:
        - "raise": raise a ValueError
        - "ignore": ignore the message
        - a callable that will be called with the invalid message as argument
    :param timeout: The timeout in seconds to use when waiting for a reply
    """

    def __init__(self, prefix: str, command_input: TextIO, command_output: TextIO, commands_handler: Callable[[str, str, list], Any] | CommandRegister, on_invalid_message: str | Callable[[str], None] = "raise", timeout: float = 5):
        super().__init__(prefix, commands_handler, on_invalid_message, timeout)
        self.command_input = command_input
        self.command_output = command_output

        self._poll_message_thread = threading.Thread(target=self._poll_message)
        self._poll_message_thread.daemon = True
        self._poll_message_thread.start()

    def _send_message_to_other_side(self, message: str) -> None:
        print(message, file=self.command_output)

    def _poll_message(self):
        while True:
            message = self.command_input.readline().strip()
            if message:
                self._on_message(message)

