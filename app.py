import asyncio
import logging
import os

from AirthingsWavePlus.airthings_wave_plus import read_sensor_data


async def read_and_process_sensor_data(wave_plus_bluetooth_mac_address):
    sensor_measurement = await read_sensor_data(wave_plus_bluetooth_mac_address)

    publish_to_kafka = os.environ.get("PUBLISH_TO_KAFKA", "false").lower == "true"
    log.info("Publish to Kafka: {}".format(publish_to_kafka))

    publish_to_mqtt = os.environ.get("PUBLISH_TO_MQTT", "false").lower == "true"
    log.info("Publish to MQTT: {}".format(publish_to_mqtt))


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    log = logging.getLogger("app")

    airthings_wave_plus_bluetooth_mac_address = os.environ.get("AIRTHINGS_WAVE_PLUS_BLUETOOTH_MAC_ADDR")
    log.debug("Airthings Wave Plus Bluetooth MAC Address: {}".format(airthings_wave_plus_bluetooth_mac_address))

    asyncio.run(read_and_process_sensor_data(airthings_wave_plus_bluetooth_mac_address))
