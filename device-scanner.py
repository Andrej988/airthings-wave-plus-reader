import logging

import asyncio
from bleak import BleakScanner


async def scan_for_devices():
    log.info("Scanning for devices...")
    devices = await BleakScanner.discover(timeout=10.0)
    log.info("Scanning complete.")
    for device in devices:
        log.info("Found device: {}".format(device))


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    log = logging.getLogger("device-scanner")
    asyncio.run(scan_for_devices())

