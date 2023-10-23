import threading
from typing import Callable, Any, TextIO
from tacticom import tactiprotocol
from uuid import uuid4


class CommandRegister:
    commands: dict[str, Callable[[str, list], Any]] = {}

    def register(self, command: str, handler: Callable[[str, list], Any]):
        self.commands[command] = handler

    def __call__(self, command: str, ask_code: str, arguments: list):
        if command in self.commands:
            return self.commands[command](ask_code, *arguments)
        else:
            raise ValueError(f"Invalid command: {command}")


class TactiCom:
    def __init__(self, prefix: str, commands_handler: Callable[[str, str, list], Any] | CommandRegister, send_callback: Callable[[str], None]):
        self.prefix = prefix
        self.commands_handler = commands_handler
        self.send_callback = send_callback
        self.in_waiting: dict[str, threading.Event] = {}
        self.results = {}

    def _on_message(self, message_str: str):
        try:
            message = tactiprotocol.parse(message_str)

            if message.prefix != self.prefix:
                raise ValueError(f"Invalid prefix: {message.prefix} (expected: {self.prefix})")
        except ValueError:
            print("Invalid message: " + message_str)
            return

        if message.answer_code in self.in_waiting:
            self.in_waiting.pop(message.answer_code).set()
            self.results[message.answer_code] = message.command, message.arguments
        else:
            self.commands_handler(message.command, message.ask_code, message.arguments)

    def send(self, answer_code: str | None, command: str, ask_code: str | None, *args):
        self.send_callback(tactiprotocol.serialize(tactiprotocol.TactiMessage(self.prefix, answer_code, command, ask_code, list(args))))

    def send_message(self, message: str, *args):
        self.send(None, message, None, *args)

    async def ask_message(self, message: str, *args):
        guid = str(uuid4())
        event = threading.Event()
        self.in_waiting[guid] = event
        self.send(None, message, guid, *args)
        event.wait()
        return self.results.pop(guid)

    def answer_message(self, answer_code: str, message: str, *args):
        self.send(answer_code, message, None, *args)


class SerialTactiCom(TactiCom):
    def __init__(self, prefix: str, port: str, baudrate: int, commands_handler: Callable[[str, str, list], Any] | CommandRegister, reader_sleep_time: float = 0.1):
        super().__init__(prefix, commands_handler, self._send)

        from tacticom import TactiSerial
        self._ts = TactiSerial(port, baudrate, self._on_message, reader_sleep_time=reader_sleep_time)

    def _send(self, message: str):
        self._ts.send(message)

    def open(self):
        self._ts.open()

    def close(self):
        self._ts.close()


class SubprocessTactiCom(TactiCom):
    def __init__(self, prefix: str, command_input: TextIO, command_output: TextIO, commands_handler: Callable[[str, list], Any] | CommandRegister):
        super().__init__(prefix, commands_handler, lambda message: print(message, file=command_output))

        self.command_input = command_input
        self.check_for_message_thread = threading.Thread(target=self.check_for_message)
        self.check_for_message_thread.daemon = True
        self.check_for_message_thread.start()

    def check_for_message(self):
        while True:
            message = self.command_input.readline().strip()
            self._on_message(message)
