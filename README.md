# Airthings Wave Plus Reader 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Application which periodically reading Airthings Wave Plus sensor measurement over Bluetooth Low Energy (BLE) and publish them to MQTT and/or Apache Kafka.

Airthings Wave Plus is a smart IAQ monitor with Radon detection, including sensosr for temperature, humidity, air pressure, TVOCs and CO2.

This project was inspired by:
* https://github.com/Airthings/waveplus-reader
* https://github.com/custom-components/sensor.airthings_wave

**Table of contents**
- [Airthings Wave Plus Reader/Publisher](#airthings-wave-plus-reader)
- [Sensor data description](#sensor-data-description)
- [Prerequisites](#prerequisites)
- [Python Dependencies](#python-dependencies)
- [BLE Scanning](#ble-scanning)
- [Configuration](#configuration)
- [Output message format](#output-message-format)
- [Testing](#testing)
- [License](#license)

### Sensor data description
| Sensor                        | Unit of measurement                 | Comments                                                       |
|-------------------------------|-------------------------------------|----------------------------------------------------------------|
| Temperature                   | Degrees Celsius (&deg;C)            |                                                                |
| Humidity                      | Relative Humidity (%rH)             |                                                                |
| Radon short term average      | Becquerel per cubic metre (Bq/m3)   | First measurement available one hour after inserting batteries |
| Radon long term average       | Becquerel per cubic metre (Bq/m3)   | First measurement available one hour after inserting batteries |
| Relative atmospheric pressure | Hectopascal (hPa) / millibar (mbar) | 1 hPa is equal to 1 mbar                                       |
| CO2 level                     | particles per million (ppm)         |                                                                |
| TVOC level                    | particles per billion (ppb)         | Total volatile organic compounds level                         |


### Prerequisites
* Airthings Wave Plus: Smart, battery operated, indoor air quality monitor (https://www.airthings.com/en/wave-plus)
* MQTT broker (optional)
* Kafka broker (optional)

### Python Dependencies
| Dependency    | Description                            | Version |
|---------------|----------------------------------------|---------|
| PyYaml        | Processing YAML configuration file     | 6.0     |
| bleak         | Library for Bluetooth Low Energy (BLE) | 0.18.1  |
| bleak-winrt   | Library for Bluetooth Low Energy (BLE) | 1.2.0   |
| async-timeout | Used by bleak library                  | 4.0.2   |
| kafka-python3 | Library used for publishing to kafka   | 3.0.0   |
| paho-mqtt     | library used for publishing to MQTT    | 1.6.1   |


### BLE Scanning
There are two scanning modes available:
* Scanning for predefined Airthings Wave Plus Bluetooth MAC Address
  * MAC address should be entered in config.yml 
  * You can use device-scanner.py for scanning all available devices to find out MAC address
* Scanning for predefined 10-digit Airthings Wave Plus Serial Number
  * Serial number can be found under the magnetic backplate of your Airthings Wave Plus

### Configuration
Configuration of application is done via YAML file named config.yml.
You can use configuration template file (config-template.yml) which includes all available configuration options. Note: Final configuration file should be saved as config.yml.

### Output message format
```json
{
  "sensor_name": "Airthings Wave Plus",
  "sensor_bluetooth_mac_address": "REDACTED",
  "sensor_serial_number": "REDACTED",
  "sensor_version": 1,
  "timestamp": "2022-10-11T19:24:43.424432",
  "temperature": {
    "value": 25.77,
    "unit": "degC"
  },
  "humidity": {
    "value": 50.5,
    "unit": "%rH"
  },
  "pressure": {
    "value": 992.86,
    "unit": "hPa"
  },
  "radon_short_term_avg": {
    "value": 90,
    "unit": "Bq/m3"
  },
  "radon_long_term_avg": {
    "value": 100,
    "unit": "Bq/m3"
  },
  "co2_level": {
    "value": 925,
    "unit": "ppm"
  },
  "voc_level": {
    "value": 256,
    "unit": "ppb"
  },
  "battery_level": {
    "value": 100,
    "unit": "%"
  }
}
```

### Testing
Application was tested using:
* Windows 10
* Python 3.10
* Mosquitto MQTT (using SSL with authentication)
* Apache Kafka (SASL_SSL PLAIN mechanism).

### License
MIT License

Copyright (c) 2022 Andrej988

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


