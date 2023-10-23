import asyncio
import time

from tacticom import SerialTactiCom
from tacticom.tacticoms import CommandRegister


async def main():
    cr = CommandRegister()
    cr.register("divide_result", lambda ask_code, q, r: print("The result is: " + q + " r: " + r))

    tacticom = SerialTactiCom("R1", "/dev/ttyUSB0", 115200, cr)
    tacticom.open()
    print("Connected to TactiCom device")
    time.sleep(2)  # Let Arduino time to boot (Arduino resets on serial connection)

    tacticom.send_message("led", "on")
    print(await tacticom.ask_message("ping"))
    result = await tacticom.ask_message("add", "1", "2")
    print("The result is: " + result[1][0])
    tacticom.send_message("divide", "11", "5")
    tacticom.send_message("led", "off")
    while True:
        if input() == "exit":
            break

    tacticom.close()


if __name__ == '__main__':
    asyncio.run(main())
