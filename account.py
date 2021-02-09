class Account:

    @property
    def readings(self):
        return self._readings

    @readings.setter
    def readings(self, readings):
        self._readings = readings