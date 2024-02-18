"""
This example demonstrates how to use TextIOTactiCom to communicate with a child process.
This is the child process. Please see SubprocessTactiComExample.py for the parent process.
This script isn't intended to be run directly, but by the parent process.
"""

import os
import sys

from tacticom import TextIOTactiCom

if __name__ == '__main__':
    # Get communication pipes from launch arguments
    if len(sys.argv) != 3:
        raise ValueError("This script must be launched by the parent process with two file descriptors as arguments")
    infile = os.fdopen(int(sys.argv[1]))
    outfile = os.fdopen(int(sys.argv[2]), 'w', buffering=1)

    # Open the communication through TacitCom
    tc = TextIOTactiCom("R1", infile, outfile)

    # Register commands
    tc.get_command_register().on_request("add", lambda a, b: ("result", str(int(a) + int(b))))
    tc.get_command_register().on_event("quit", lambda: exit())

    while True:
        pass
