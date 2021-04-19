from drone_print import GenericPDrone
from drone_print import drone_print
import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
)


async def run():
    pdrone = await GenericPDrone.create()
    with open("sample_input.pfile") as sample_input:
        await drone_print(pdrone, sample_input)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())