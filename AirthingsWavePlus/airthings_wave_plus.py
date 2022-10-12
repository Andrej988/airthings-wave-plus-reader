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
import struct
from datetime import datetime

from bleak import BleakScanner, BleakClient

from AirthingsWavePlus.sensor_measurement import SensorMeasurement
from AirthingsWavePlus.sensor_measurements import SensorMeasurements

# Handle 02: 00002a00-0000-1000-8000-00805f9b34fb (Handle: 2): Device Name
GATT_CHAR_HANDLE_DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb"

# Handle 12: b42e2a68-ade7-11e4-89d3-123b93f75cba (Handle: 12): Current Sensor ValuesOAD Extended Control
GATT_CHAR_HANDLE_CURRENT_SENSOR_VALUES = "b42e2a68-ade7-11e4-89d3-123b93f75cba"
CURRENT_SENSOR_VALUES_FORMAT = '<BBBBHHHHHHHH'

# Handle 15: b42e2d06-ade7-11e4-89d3-123b93f75cba (Handle: 15): Access Control Point
GATT_CHAR_HANDLE_ACCESS_CONTROL_POINT = "b42e2d06-ade7-11e4-89d3-123b93f75cba"
ACCESS_CONTROL_POINT_RESPONSE_FORMAT = '<L12B6H'

# Handle 39: 00002a24-0000-1000-8000-00805f9b34fb (Handle: 39): Model Number String
GATT_CHAR_HANDLE_DEVICE_MODEL_NUMBER_STRING = "00002a24-0000-1000-8000-00805f9b34fb"

# Handle 43: 00002a26-0000-1000-8000-00805f9b34fb (Handle: 43): Firmware Revision String
GATT_CHAR_HANDLE_DEVICE_FIRMWARE_REVISION_STRING = "00002a26-0000-1000-8000-00805f9b34fb"

# Handle 45: 00002a27-0000-1000-8000-00805f9b34fb (Handle: 45): Hardware Revision String
GATT_CHAR_HANDLE_DEVICE_HARDWARE_REVISION_STRING = "00002a27-0000-1000-8000-00805f9b34fb"

# Handle 47: 00002a29-0000-1000-8000-00805f9b34fb (Handle: 47): Manufacturer Name String
GATT_CHAR_HANDLE_DEVICE_MANUFACTURER_NAME_STRING = "00002a29-0000-1000-8000-00805f9b34fb"


class AirthingsWavePlus:
    def __init__(self, wave_plus_bluetooth_mac_address, wave_plus_serial_number):
        self.class_name = "AirthingsWavePlus"
        self.device_data = {}
        self.control_point_data = {}
        self.sensor_measurement_data = {}
        self.event = set()
        self.device_mac_address = wave_plus_bluetooth_mac_address
        self.device_serial_number = wave_plus_serial_number

    async def __scan_for_device(self):
        if self.device_mac_address is not None:
            device = await self.__scan_for_device_mac_address()
            self.device_data['bluetooth_mac_addr'] = self.device_mac_address
            self.device_data['serial_number'] = self.__extract_serial_number(device)
            return device

        elif self.device_serial_number is not None:
            device = await self.__scan_for_device_serial_number()
            self.device_data['bluetooth_mac_addr'] = device.address
            self.device_data['serial_number'] = self.device_serial_number
            return device

        else:
            raise Exception("Missing device information. "
                            "Please enter either device bluetooth MAC address or serial number.")

    async def __scan_for_device_mac_address(self):
        log = logging.getLogger(self.class_name + ".__scan_for_device_mac_address")
        log.info("Scanning for device with MAC Address: {}".format(self.device_mac_address))
        device = await BleakScanner.find_device_by_address(self.device_mac_address)
        if device is None:
            raise Exception("Device not found!!!")
        log.info("Scanning complete [device found]...")
        return device

    async def __scan_for_device_serial_number(self):
        log = logging.getLogger(self.class_name + ".__scan_for_device_serial_number")
        log.info("Scanning for device with serial number: {}".format(self.device_serial_number))
        advertisements = await BleakScanner.discover(timeout=5)
        log.info("Scanning complete...")
        device = None

        for advertisement in advertisements:
            log.info("Available device: {}".format(advertisement))
            if 820 in advertisement.metadata['manufacturer_data']:
                log.debug(advertisement.metadata['manufacturer_data'])
                serial_number = self.__extract_serial_number(advertisement)
                if serial_number == self.device_serial_number:
                    log.info("Device found: {0}".format(advertisement))
                    print(advertisement)
                    device = advertisement

        if device is None:
            raise Exception("Device not found!!!")
        return device

    def __extract_serial_number(self, device):
        log = logging.getLogger(self.class_name + ".__extract_serial_number")
        log.debug(device.metadata['manufacturer_data'])
        serial_number_bytes = device.metadata['manufacturer_data'].get(820)
        log.debug(serial_number_bytes)
        serial_number = struct.unpack_from('<I', serial_number_bytes)
        log.info("Extracted serial number: {0}".format(serial_number[0]))
        return serial_number[0]

    def __log_client_characteristics(self, client):
        log = logging.getLogger(self.class_name + ".__log_client_characteristics")
        for char in client.services:
            for x in char.characteristics:
                log.info("Characteristic: {}".format(x))
                log.info("Description: {}".format(x.description))
                log.info("--------------------------------------")

    async def __retrieve_and_process_device_info_data(self, client):
        log = logging.getLogger(self.class_name + ".__retrieve_and_process_device_info_data")

        device_name_raw = await client.read_gatt_char(GATT_CHAR_HANDLE_DEVICE_NAME)
        self.device_data['name'] = device_name_raw.decode("utf-8")

        model_number_raw = await client.read_gatt_char(GATT_CHAR_HANDLE_DEVICE_MODEL_NUMBER_STRING)
        self.device_data['model'] = model_number_raw.decode("utf-8")

        firmware_revision_raw = await client.read_gatt_char(GATT_CHAR_HANDLE_DEVICE_FIRMWARE_REVISION_STRING)
        self.device_data['firmware_revision'] = firmware_revision_raw.decode("utf-8")

        hardware_revision_raw = await client.read_gatt_char(GATT_CHAR_HANDLE_DEVICE_HARDWARE_REVISION_STRING)
        self.device_data['hardware_revision'] = hardware_revision_raw.decode("utf-8")

        manufacturer_name_raw = await client.read_gatt_char(GATT_CHAR_HANDLE_DEVICE_MANUFACTURER_NAME_STRING)
        self.device_data['manufacturer_name'] = manufacturer_name_raw.decode("utf-8")

    async def __retrieve_and_process_access_control_point_data(self, client):
        log = logging.getLogger(self.class_name + ".__retrieve_access_control_point_data")
        self.event = asyncio.Event()
        await client.start_notify(
            GATT_CHAR_HANDLE_ACCESS_CONTROL_POINT,
            self.__access_control_point_notification_handler)
        await client.write_gatt_char(GATT_CHAR_HANDLE_ACCESS_CONTROL_POINT, struct.pack('<B', 0x6d))
        try:
            await asyncio.wait_for(self.event.wait(), 1)
        except asyncio.TimeoutError:
            log.warning("Timeout while retrieving access control point data.")
        await client.stop_notify(GATT_CHAR_HANDLE_ACCESS_CONTROL_POINT)

    def __access_control_point_notification_handler(self, sender, control_point_raw_data):
        self.event.set()
        log = logging.getLogger(self.class_name + ".__notification_handler")
        log.debug("Data: {}".format(control_point_raw_data))

        if control_point_raw_data is None:
            log.warning("Missing control point data!!!")
            return

        raw_data = control_point_raw_data[2:]
        if len(raw_data) != struct.calcsize(ACCESS_CONTROL_POINT_RESPONSE_FORMAT):
            log.warning("Data length ({0}) is not according to format length ({1})!!!".format(
                len(raw_data),
                struct.calcsize(ACCESS_CONTROL_POINT_RESPONSE_FORMAT)))
            return

        unpacked_data = struct.unpack(ACCESS_CONTROL_POINT_RESPONSE_FORMAT, raw_data)
        self.control_point_data['illuminance'] = SensorMeasurement(unpacked_data[2], "???")
        self.control_point_data['ambient_light'] = SensorMeasurement(unpacked_data[3], "???")
        self.control_point_data['measurement_periods'] = SensorMeasurement(unpacked_data[5], "???")
        voltage = unpacked_data[17] / 1000.0
        self.control_point_data['voltage'] = SensorMeasurement(voltage, "V")

        voltage_min = 2.0
        voltage_max = 3.0
        battery_level = max(0, min(100, round((voltage - voltage_min) / (voltage_max - voltage_min) * 100)))
        self.control_point_data['battery_level'] = SensorMeasurement(battery_level, "%")

    async def __retrieve_and_process_current_sensor_measurement_data(self, client):
        sensor_byte_data = await client.read_gatt_char(GATT_CHAR_HANDLE_CURRENT_SENSOR_VALUES)
        sensor_raw_data = struct.unpack(CURRENT_SENSOR_VALUES_FORMAT, sensor_byte_data)
        self.device_data['sensor_version'] = sensor_raw_data[0]
        self.sensor_measurement_data['timestamp'] = datetime.now()

        if self.device_data['sensor_version'] == 1:
            self.sensor_measurement_data['temperature'] = SensorMeasurement(sensor_raw_data[6] / 100.0, "degC")
            self.sensor_measurement_data['humidity'] = SensorMeasurement(sensor_raw_data[1] / 2.0, "%rH")
            self.sensor_measurement_data['pressure'] = SensorMeasurement(sensor_raw_data[7] / 50.0, "hPa")
            self.sensor_measurement_data['radon_short_term_avg'] = \
                SensorMeasurement(self.__conv2radon(sensor_raw_data[4]), "Bq/m3")
            self.sensor_measurement_data['radon_long_term_avg'] = \
                SensorMeasurement(self.__conv2radon(sensor_raw_data[5]), "Bq/m3")
            self.sensor_measurement_data['co2_level'] = SensorMeasurement(sensor_raw_data[8] * 1.0, "ppm")
            self.sensor_measurement_data['voc_level'] = SensorMeasurement(sensor_raw_data[9] * 1.0, "ppb")
        else:
            raise Exception("Unknown sensor version: {}".format(self.sensor_measurement_data['sensor_version']))

    def __conv2radon(self, radon_raw):
        radon = "N/A"  # Either invalid measurement, or not available
        if 0 <= radon_raw <= 16383:
            radon = radon_raw
        return radon

    async def read_sensor_data(self) -> SensorMeasurements:
        log = logging.getLogger(self.class_name + ".read_sensor_data")
        device = await self.__scan_for_device()

        log.info("Connecting to device: {}".format(self.device_mac_address))
        async with BleakClient(device, timeout=15) as client:
            log.info("Device connected...")

            # List device characteristics
            # self.__log_client_characteristics(client)

            # Retrieving and processing device data
            await self.__retrieve_and_process_device_info_data(client)
            await self.__retrieve_and_process_access_control_point_data(client)
            await self.__retrieve_and_process_current_sensor_measurement_data(client)

            measurements = SensorMeasurements(self.device_data, self.sensor_measurement_data, self.control_point_data)

            log.info("Device name: {0}".format(measurements.get_device_name()))
            log.info("Device model: {0}".format(measurements.get_device_model()))
            log.info("Device sensor version: {0}".format(measurements.get_device_sensor_version()))
            log.info("Device Bluetooth MAC address: {0}".format(measurements.get_device_bluetooth_mac_address()))
            log.info("Device Serial Number: {0}".format(measurements.get_device_serial_number()))
            log.info("Measurement timestamp: {0}".format(measurements.get_timestamp().isoformat()))
            log.info("Temperature: {0} {1}".format(
                measurements.get_temperature().value,
                measurements.get_temperature().unit))
            log.info("Humidity: {0} {1}".format(
                measurements.get_humidity().value,
                measurements.get_humidity().unit))
            log.info("Pressure: {0} {1}".format(
                measurements.get_pressure().value,
                measurements.get_pressure().unit))
            log.info("Radon short term average: {0} {1}".format(
                measurements.get_radon_short_term_average().value,
                measurements.get_radon_short_term_average().unit))
            log.info("Radon long term average: {0} {1}".format(
                measurements.get_radon_long_term_average().value,
                measurements.get_radon_long_term_average().unit))
            log.info("CO2 Level: {0} {1}".format(
                measurements.get_co2_level().value,
                measurements.get_co2_level().unit))
            log.info("VOC Level: {0} {1}".format(
                measurements.get_voc_level().value,
                measurements.get_voc_level().unit))
            log.info("Illuminance: {0} {1}".format(
                measurements.get_illuminance().value,
                measurements.get_illuminance().unit))
            log.info("Ambient light: {0} {1}".format(
                measurements.get_ambient_light().value,
                measurements.get_ambient_light().unit))
            log.info("Measurement period: {0} {1}".format(
                measurements.get_measurement_periods().value,
                measurements.get_measurement_periods().unit))
            log.info("Voltage: {0} {1}".format(
                measurements.get_device_voltage().value,
                measurements.get_device_voltage().unit))
            log.info("Battery level: {0} {1}".format(
                measurements.get_device_battery_level().value,
                measurements.get_device_battery_level().unit))

            return measurements
