class Account:

    @property
    def readings(self):
        return self._readings

    @readings.setter
    def readings(self, readings):
        self._readings = readings

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, member):
        self._member = member