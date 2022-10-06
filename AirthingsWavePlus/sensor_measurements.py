from datetime import datetime

from AirthingsWavePlus.sensor_measurement import SensorMeasurement


def conv2radon(radon_raw):
    radon = "N/A"  # Either invalid measurement, or not available
    if 0 <= radon_raw <= 16383:
        radon = radon_raw
    return radon


class SensorMeasurements:
    def __init__(self, sensor_bluetooth_mac_addr, raw_sensor_data):
        self.sensor_version = raw_sensor_data[0]
        self.sensor_bluetooth_mac_address = sensor_bluetooth_mac_addr
        self.timestamp = datetime.now()
        if self.sensor_version == 1:
            self.temperature = SensorMeasurement(raw_sensor_data[6] / 100.0, "degC")
            self.humidity = SensorMeasurement(raw_sensor_data[1] / 2.0, "%rH")
            self.pressure = SensorMeasurement(raw_sensor_data[7] / 50.0, "hPa")
            self.radon_short_term_avg = SensorMeasurement(conv2radon(raw_sensor_data[4]), "Bq/m3")
            self.radon_long_term_avg = SensorMeasurement(conv2radon(raw_sensor_data[5]), "Bq/m3")
            self.co2_level = SensorMeasurement(raw_sensor_data[8] * 1.0, "ppm")
            self.voc_level = SensorMeasurement(raw_sensor_data[9] * 1.0, "ppb")
        else:
            print("ERROR: Unknown sensor version...")

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
