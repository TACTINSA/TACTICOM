import asyncio
import os
import subprocess
import time

from tacticom import CommandRegister, SubprocessTactiCom


async def main():
    (r1, w1) = os.pipe2(0)  # for parent -> child writes
    (r2, w2) = os.pipe2(0)  # for child -> parent writes
    child = subprocess.Popen(['python3', './SubprocessTactiComExampleChild.py', str(r1), str(w2)], pass_fds=(r1, w2))
    outfile = os.fdopen(w1, 'w', buffering=1)
    infile = os.fdopen(r2)

    tc = SubprocessTactiCom("R1", infile, outfile, CommandRegister())
    result = await tc.send_request("add", 1, "2")
    print(result[1][0])
    time.sleep(1)
    print(await tc.send_request("add", 3, 4))

    tc.send_event("quit")
    child.wait()

if __name__ == '__main__':
    asyncio.run(main())
