"""
This example demonstrates how to use TextIOTactiCom to communicate with a child process.
"""

import os
import subprocess

from tacticom import TextIOTactiCom


def main():
    # Spawn process python3 ./SubprocessTactiComExampleChild.py
    # r1 and w2 enable communication and must be transferred as launch argument to the child process
    (r1, w1) = os.pipe2(0)  # for parent -> child writes
    (r2, w2) = os.pipe2(0)  # for child -> parent writes
    child = subprocess.Popen(['python3', './SubprocessTactiComExampleChild.py', str(r1), str(w2)], pass_fds=(r1, w2))

    # Open the communication pipes
    outfile = os.fdopen(w1, 'w', buffering=1)
    infile = os.fdopen(r2)

    # Create a TextIOTactiCom
    tc = TextIOTactiCom("R1", infile, outfile)

    # Send a test command and print the result
    answer_command, answer_parameters = tc.send_request("add", 1, "2")
    print(f"Computed from child process: 1 + 2 = {answer_parameters[0]}")

    # Exit properly by sending a quit event and waiting for the child process to terminate
    tc.send_event("quit")
    child.wait()


if __name__ == '__main__':
    main()  # Run the main function (asyncio allows to use async/await in the main function)
