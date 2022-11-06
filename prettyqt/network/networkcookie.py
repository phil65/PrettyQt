from __future__ import annotations

import dateutil.parser

from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import bidict, types


RAW_FORMS = bidict(
    name_and_value_only=QtNetwork.QNetworkCookie.RawForm.NameAndValueOnly,
    full=QtNetwork.QNetworkCookie.RawForm.Full,
)


class NetworkCookie(QtNetwork.QNetworkCookie):
    def __repr__(self):
        return f"{type(self).__name__}({self.name()}, {self.value()})"

    def to_raw_form(self, full: bool = True):
        form = RAW_FORMS["full"] if full else RAW_FORMS["name_and_value_only"]
        self.toRawForm(form)

    def set_name(self, name: types.ByteArrayType):
        if isinstance(name, str):
            name = name.encode()
        if isinstance(name, bytes):
            name = QtCore.QByteArray(name)
        self.setName(name)

    def get_name(self) -> str:
        return bytes(self.name()).decode()

    def set_value(self, value: types.ByteArrayType):
        if isinstance(value, str):
            value = value.encode()
        if isinstance(value, bytes):
            value = QtCore.QByteArray(value)
        self.setValue(value)

    def get_value(self) -> str:
        return bytes(self.value()).decode()

    def set_expiration_date(self, date: types.DateTimeType | None):
        if date is None:
            date = QtCore.QDateTime()
        elif isinstance(date, str):
            date = dateutil.parser.parse(date)
        self.setExpirationDate(date)  # type: ignore


if __name__ == "__main__":
    cookie = NetworkCookie()
    print(repr(cookie))
