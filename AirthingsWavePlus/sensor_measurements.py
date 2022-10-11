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
    def __init__(self, sensor_data, control_point_data):
        self.sensor_version = sensor_data['sensor_version']
        self.sensor_bluetooth_mac_address = sensor_data['sensor_bluetooth_mac_addr']
        self.sensor_serial_number = sensor_data['sensor_serial_number']
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
        self.voltage = control_point_data['voltage']
        self.battery_level = control_point_data['battery_level']

    def getSensorBluetoothMACAddress(self):
        return self.sensor_bluetooth_mac_address

    def getSensorSerialNumber(self):
        return self.sensor_serial_number

    def getSensorVersion(self):
        return self.sensor_version

    def getSensorBluetoothMACAddress(self):
        return self.sensor_bluetooth_mac_address

    def getTimestamp(self):
        return self.timestamp

    def getTemperature(self):
        return self.temperature

    def getHumidity(self):
        return self.humidity

    def getPressure(self):
        return self.pressure

    def getRadonShortTermAverage(self):
        return self.radon_short_term_avg

    def getRadonLongTermAverage(self):
        return self.radon_long_term_avg

    def getCO2Level(self):
        return self.co2_level

    def getVOCLevel(self):
        return self.voc_level

    def getIlluminance(self):
        return self.illuminance

    def getAmbientLight(self):
        return self.ambient_light

    def getMeasurementPeriods(self):
        return self.measurement_periods

    def getVoltage(self):
        return self.voltage

    def getBatteryLevel(self):
        return self.battery_level

    def toJson(self):
        measurement_object = {
            "sensor_bluetooth_mac_address": self.sensor_bluetooth_mac_address,
            "sensor_serial_number": self.sensor_serial_number,
            "sensor_version": self.sensor_version,
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
            },
            "battery_level": {
                "value": self.battery_level.value,
                "unit": self.battery_level.unit
            }
        }
        return json.dumps(measurement_object, indent=2, sort_keys=False, default=str, separators=(',', ':'))\
            .encode('utf-8')
