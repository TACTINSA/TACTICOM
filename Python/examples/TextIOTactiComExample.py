"""
This example demonstrates how to use TextIOTactiCom to communicate in a console.
"""

import sys

from tacticom import TextIOTactiCom

if __name__ == '__main__':
    # Open the communication through TacitCom using stdin and stdout (console in and out)
    tc = TextIOTactiCom("R1", sys.stdin, sys.stdout, on_invalid_message="ignore")

    # Register commands
    tc.get_command_register().on_request("add", lambda a, b: ("result", str(int(a) + int(b))))
    tc.get_command_register().on_event("quit", lambda: exit())

    while True:  # Wait for commands to be received from the console
        pass
