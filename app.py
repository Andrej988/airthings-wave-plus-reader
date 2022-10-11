# MIT License
# Copyright (c) 2022 Andrej988
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import logging
import os

from AirthingsWavePlus.airthings_wave_plus import AirthingsWavePlus


async def read_and_process_sensor_data(wave_plus_bluetooth_mac_address, airthings_wave_plus_serial_number):
    airthings_wave_sensor = AirthingsWavePlus(wave_plus_bluetooth_mac_address, airthings_wave_plus_serial_number)
    sensor_measurement = await airthings_wave_sensor.read_sensor_data()

    print(sensor_measurement.toJson())

    publish_to_kafka = os.environ.get("PUBLISH_TO_KAFKA", "false").lower == "true"
    log.info("Publish to Kafka: {}".format(publish_to_kafka))

    publish_to_mqtt = os.environ.get("PUBLISH_TO_MQTT", "false").lower == "true"
    log.info("Publish to MQTT: {}".format(publish_to_mqtt))


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    log = logging.getLogger("app")

    airthings_wave_plus_bluetooth_mac_address = os.environ.get("AIRTHINGS_WAVE_PLUS_BLUETOOTH_MAC_ADDR")
    log.debug("Airthings Wave Plus Bluetooth MAC Address: {}".format(airthings_wave_plus_bluetooth_mac_address))

    airthings_wave_plus_serial_number = os.environ.get("AIRTHINGS_WAVE_PLUS_SERIAL_NUMBER")
    log.debug("Airthings Wave Plus Serial Number: {}".format(airthings_wave_plus_serial_number))

    asyncio.run(read_and_process_sensor_data(airthings_wave_plus_bluetooth_mac_address,airthings_wave_plus_serial_number))
