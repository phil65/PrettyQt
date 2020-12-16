import datetime
from typing import Union

from qtpy import QtCore, QtNetwork

from prettyqt.utils import bidict


RAW_FORMS = bidict(
    name_and_value_only=QtNetwork.QNetworkCookie.NameAndValueOnly,
    full=QtNetwork.QNetworkCookie.Full,
)


class NetworkCookie(QtNetwork.QNetworkCookie):
    def __repr__(self):
        return f"{type(self).__name__}({self.name()}, {self.value()})"

    def to_raw_form(self, full: bool = True):
        form = RAW_FORMS["full"] if full else RAW_FORMS["name_and_value_only"]
        self.toRawForm(form)

    def set_name(self, name: str):
        self.setName(name.encode())

    def get_name(self) -> str:
        return bytes(self.name()).decode()

    def set_value(self, value: str):
        self.setValue(value.encode())

    def get_value(self) -> str:
        return bytes(self.value()).decode()

    def set_expiration_date(self, date: Union[QtCore.QDateTime, datetime.datetime, None]):
        if date is None:
            date = QtCore.QDateTime()
        self.setExpirationDate(date)


if __name__ == "__main__":
    cookie = NetworkCookie()
    print(repr(cookie))
