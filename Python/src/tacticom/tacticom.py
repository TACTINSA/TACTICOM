from typing import Callable, Any


class TactiCom:
    def __init__(self, prefix: str, port: str, baudrate: int, commands_handler: Callable[[str, list], Any], reader_sleep_time: float = 0.1):
        self.prefix = prefix + "+"
        self.commands_handler = commands_handler

        from src.tacticom import TactiSerial
        self._ts = TactiSerial(port, baudrate, self._on_message, reader_sleep_time=reader_sleep_time)

    def _on_message(self, message):
        if not message.startswith(self.prefix):
            print("Received invalid message: " + message)
            return

        message = message[len(self.prefix):]

        if "=" in message:
            command, args = message.split("=")
            args = args.split(",")
        else:
            command = message
            args = []

        self.commands_handler(command, args)

    def open(self):
        self._ts.open()

    def close(self):
        self._ts.close()

    def send(self, command: str, *args):
        message = self.prefix + command
        if args:
            message += "=" + ",".join(args)
        self._ts.send(message)
