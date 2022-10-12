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

import json


class SensorMeasurements:
    def __init__(self, device_data, sensor_data, control_point_data):
        self.device_name = device_data['name']
        self.device_model = device_data['model']
        self.device_bluetooth_mac_address = device_data['bluetooth_mac_addr']
        self.device_serial_number = device_data['serial_number']
        self.device_hardware_revision = device_data['hardware_revision']
        self.device_firmware_revision = device_data['firmware_revision']
        self.device_manufacturer_name = device_data['manufacturer_name']
        self.device_sensor_version = device_data['sensor_version']

        self.timestamp = sensor_data['timestamp']
        self.temperature = sensor_data['temperature'];
        self.humidity = sensor_data['humidity']
        self.pressure = sensor_data['pressure']
        self.radon_short_term_avg = sensor_data['radon_short_term_avg']
        self.radon_long_term_avg = sensor_data['radon_long_term_avg']
        self.co2_level = sensor_data['co2_level']
        self.voc_level = sensor_data['voc_level']

        self.illuminance = control_point_data['illuminance']
        self.ambient_light = control_point_data['ambient_light']
        self.measurement_periods = control_point_data['measurement_periods']
        self.device_voltage = control_point_data['voltage']
        self.device_battery_level = control_point_data['battery_level']

    def get_device_name(self):
        return self.device_name

    def get_device_model(self):
        return self.device_model

    def get_device_bluetooth_mac_address(self):
        return self.device_bluetooth_mac_address

    def get_device_serial_number(self):
        return self.device_serial_number

    def get_device_sensor_version(self):
        return self.device_sensor_version

    def get_device_hardware_revision(self):
        return self.device_hardware_revision

    def get_device_firmware_revision(self):
        return self.device_firmware_revision

    def get_device_manufacturer_name(self):
        return self.device_manufacturer_name

    def get_timestamp(self):
        return self.timestamp

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_pressure(self):
        return self.pressure

    def get_radon_short_term_average(self):
        return self.radon_short_term_avg

    def get_radon_long_term_average(self):
        return self.radon_long_term_avg

    def get_co2_level(self):
        return self.co2_level

    def get_voc_level(self):
        return self.voc_level

    def get_illuminance(self):
        return self.illuminance

    def get_ambient_light(self):
        return self.ambient_light

    def get_measurement_periods(self):
        return self.measurement_periods

    def get_device_voltage(self):
        return self.device_voltage

    def get_device_battery_level(self):
        return self.device_battery_level

    def to_json(self):
        measurement_object = {
            "device": {
                "name": self.device_name,
                "model": self.device_model,
                "manufacturer": self.device_manufacturer_name,
                "serial_num": self.device_serial_number,
                "bluetooth_MAC_addr": self.device_bluetooth_mac_address,
                "sensor_version": self.device_sensor_version,
                "hardware_revision": self.device_hardware_revision,
                "firmware_revision": self.device_firmware_revision,
                "battery_level": {
                    "value": self.device_battery_level.value,
                    "unit": self.device_battery_level.unit
                }
            },
            "measurements": {
                "timestamp": self.timestamp.isoformat(),
                "temperature": {
                    "value": self.temperature.value,
                    "unit": self.temperature.unit
                },
                "humidity": {
                    "value": self.humidity.value,
                    "unit": self.humidity.unit
                },
                "pressure": {
                    "value": self.pressure.value,
                    "unit": self.pressure.unit
                },
                "radon_short_term_avg": {
                    "value": self.radon_short_term_avg.value,
                    "unit": self.radon_short_term_avg.unit
                },
                "radon_long_term_avg": {
                    "value": self.radon_long_term_avg.value,
                    "unit": self.radon_long_term_avg.unit
                },
                "co2_level": {
                    "value": self.co2_level.value,
                    "unit": self.co2_level.unit
                },
                "voc_level": {
                    "value": self.voc_level.value,
                    "unit": self.voc_level.unit
                }
            }
        }
        return json.dumps(measurement_object, indent=2, sort_keys=False, default=str, separators=(',', ':'))\
            .encode('utf-8')
