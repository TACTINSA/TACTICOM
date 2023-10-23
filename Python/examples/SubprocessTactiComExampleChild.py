import os
import sys
import threading
from typing import Callable, Any, TextIO

from tacticom import CommandRegister, SubprocessTactiCom


def stop():
    global running
    running = False


if __name__ == '__main__':
    running = True
    infile = os.fdopen(int(sys.argv[1]))
    outfile = os.fdopen(int(sys.argv[2]), 'w', buffering=1)
    cr = CommandRegister()
    tc = SubprocessTactiCom("R1", infile, outfile, cr)
    cr.register("add", lambda ask_code, a, b: tc.answer_message(ask_code, "result", str(int(a) + int(b))))
    cr.register("quit", lambda ask_code: stop())

    while running:
        pass
