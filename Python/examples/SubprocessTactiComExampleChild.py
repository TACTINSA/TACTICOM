import os
import sys

from tacticom import CommandRegister, SubprocessTactiCom


def stop():
    global running
    running = False


if __name__ == '__main__':
    running = True
    infile = os.fdopen(int(sys.argv[1]))
    outfile = os.fdopen(int(sys.argv[2]), 'w', buffering=1)
    cr = CommandRegister()
    cr.register_reply("add", lambda a, b: ("result", str(int(a) + int(b))))
    cr.register_event("quit", stop)
    tc = SubprocessTactiCom("R1", infile, outfile, cr)

    while running:
        pass
