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
import time

import logging

from AirthingsWavePlus.airthings_wave_plus import AirthingsWavePlus
from Config.yaml_config import Config
from Kafka.kafka_publisher import KafkaPublisher
from MQTT.mqtt_publisher import MqttPublisher

start_time = time.time()


async def __read_and_process_sensor_data(config):
    log.debug("Airthings Wave Plus Bluetooth MAC Address: {0}".format(config.getAirthingsWavePlusBluetoothMACAddress()))
    log.debug("Airthings Wave Plus Serial Number: {0}".format(config.getAirthingsWavePlusSerialNumber()))

    try:
        airthings_wave_sensor = AirthingsWavePlus(
            config.getAirthingsWavePlusBluetoothMACAddress(),
            config.getAirthingsWavePlusSerialNumber())
        sensor_measurement = await airthings_wave_sensor.read_sensor_data()
    except Exception as e:
        log.error("Error during retrieval of sensor data: {0}".format(str(e)))

    log.info("Publish to Kafka: {}".format(config.getPublishToKafka()))
    if config.getPublishToKafka():
        try:
            kafka_publisher = KafkaPublisher(
                config.getKafkaBootstrapServers(),
                config.getKafkaSecurityProtocol(),
                config.getKafkaSASLMechanism(),
                config.getKafkaSSLCAFile(),
                config.getKafkaSASLUsername(),
                config.getKafkaSASLPassword())
            kafka_publisher.publish(config.getKafkaTopic(), sensor_measurement.toJson())
        except Exception as e:
            log.error("Error during publishing to Kafka: {0}".format(str(e)))

    log.info("Publish to MQTT: {0}".format(config.getPublishToMQTT()))
    if config.getPublishToMQTT():
        try:
            mqtt_publisher = MqttPublisher(
                broker_hostname=config.getMQTTHostname(),
                port=config.getMQTTPort(),
                connection_type=config.getMQTTConnectionType(),
                username=config.getMQTTUsername(),
                password=config.getMQTTPassword(),
                tls_config=config.getMQTTConfigTLS()
            )
            mqtt_publisher.publish(config.getMQTTPublishTopic(),
                                   sensor_measurement.toJson(),
                                   config.getMQTTPublishQOS(),
                                   config.getMQTTPublishRetainMsg())
        except Exception as e:
            log.error("Error during publishing to Kafka: {0}".format(str(e)))


async def __process_function_periodically(interval, periodic_function, config):
    while True:
        time_elapsed = round(time.time() - start_time)
        counter = int((time_elapsed / interval) + 1)
        log.info("Execution counter: {0}".format(counter))
        await asyncio.gather(
            asyncio.sleep(interval),
            periodic_function(config),
        )


if __name__ == "__main__":
    app_config = Config("config.yml")
    logging.basicConfig(level=app_config.getLoglevel())
    log = logging.getLogger("app")

    log.info("Scheduler delay: {0}s".format(app_config.getSchedulerDelay()))
    scheduler_delay = app_config.getSchedulerDelay() if app_config.getSchedulerDelay() is not None else 300

    asyncio.run(__process_function_periodically(scheduler_delay, __read_and_process_sensor_data, app_config))
