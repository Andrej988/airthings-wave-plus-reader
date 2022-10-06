class SensorMeasurement:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def getValue(self):
        return self.value

    def getUnit(self):
        return self.unit
