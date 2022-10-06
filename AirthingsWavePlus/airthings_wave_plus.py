import logging
import os
import struct

from bleak import BleakScanner, BleakClient
from AirthingsWavePlus.sensor_measurements import SensorMeasurements


async def read_sensor_data(wave_plus_bluetooth_mac_address) -> SensorMeasurements:
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    log = logging.getLogger("sensor_measurements.read_sensor_data")

    device = await BleakScanner.find_device_by_address(wave_plus_bluetooth_mac_address)
    log.info("Scanning complete...")

    if device is None:
        raise Exception("Device not found...")

    async with BleakClient(device, timeout=15) as client:
        log.info("Device connected...")

        # Handle 12: b42e2a68-ade7-11e4-89d3-123b93f75cba (Handle: 12): Current Sensor ValuesOAD Extended Control
        sensor_byte_data = await client.read_gatt_char(12)

        sensor_raw_data = struct.unpack('<BBBBHHHHHHHH', sensor_byte_data)
        measurements = SensorMeasurements(wave_plus_bluetooth_mac_address, sensor_raw_data)

        log.info("Sensor version: {0}".format(measurements.getSensorVersion()))
        log.info("Measurement timestamp: {0}".format(measurements.getTimestamp().isoformat()))
        log.info("Temperature: {0} {1}".format(
            measurements.getTemperature().value,
            measurements.getTemperature().unit))
        log.info("Humidity: {0} {1}".format(
            measurements.getHumidity().value,
            measurements.getHumidity().unit))
        log.info("Pressure: {0} {1}".format(
            measurements.getPressure().value,
            measurements.getPressure().unit))
        log.info("Radon short term average: {0} {1}".format(
            measurements.getRadonShortTermAverage().value,
            measurements.getRadonShortTermAverage().unit))
        log.info("Radon long term average: {0} {1}".format(
            measurements.getRadonLongTermAverage().value,
            measurements.getRadonLongTermAverage().unit))
        log.info("CO2 Level: {0} {1}".format(
            measurements.getCO2Level().value,
            measurements.getCO2Level().unit))
        log.info("VOC Level: {0} {1}".format(
            measurements.getVOCLevel().value,
            measurements.getVOCLevel().unit))

        return measurements
