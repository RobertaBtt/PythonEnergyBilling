class Account:

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

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