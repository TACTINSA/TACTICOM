import threading
import time
from typing import Callable

import serial


class TactiSerial:
    def __init__(self, port: str, baudrate: int, on_message_callback: Callable[[str], None], use_raw_callback: bool = False, poll_sleep_time: float = 0.1):
        self.port = port
        self.baudrate = baudrate
        self.on_message_callback = on_message_callback
        self.use_raw_callback = use_raw_callback
        self.poll_sleep_time = poll_sleep_time

        self._serial = serial.Serial(baudrate=self.baudrate)
        self._serial.port = self.port  # Set port after to delay ts open

    def _start_reader(self):
        """Start reader thread"""
        self._receiver_thread = threading.Thread(target=self._reader, name='rx', daemon=True)
        self._receiver_thread.start()

    def _reader(self):
        """Read from the Serial port"""
        while self._serial.is_open:
            if self._serial.inWaiting() > 0:
                if self.use_raw_callback:
                    data = self._serial.read(self._serial.inWaiting())
                else:
                    data = self._serial.readline().decode("utf-8").strip()

                self.on_message_callback(data)

            if self.poll_sleep_time:
                time.sleep(self.poll_sleep_time)

    def open(self):
        """Open Serial port connection"""
        self._serial.open()
        self._start_reader()

    def close(self):
        """Close Serial port connection"""
        self._serial.close()

    def send(self, message: str):
        """Send a message to the Serial port"""
        self._serial.write(bytes(message + "\n", 'utf-8'))

    def send_raw(self, message: bytes):
        """Send a raw message to the Serial port"""
        self._serial.write(message)
