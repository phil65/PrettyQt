from __future__ import annotations

import dateutil.parser

from prettyqt.qt import QtCore, QtNetwork
from prettyqt.utils import bidict, datatypes, get_repr


RAW_FORMS = bidict(
    name_and_value_only=QtNetwork.QNetworkCookie.RawForm.NameAndValueOnly,
    full=QtNetwork.QNetworkCookie.RawForm.Full,
)


class NetworkCookie(QtNetwork.QNetworkCookie):
    def __repr__(self):
        return get_repr(self, self.name(), self.value())

    def to_raw_form(self, full: bool = True):
        form = RAW_FORMS["full"] if full else RAW_FORMS["name_and_value_only"]
        self.toRawForm(form)

    def set_name(self, name: datatypes.ByteArrayType):
        if isinstance(name, str):
            name = name.encode()
        if isinstance(name, bytes):
            name = QtCore.QByteArray(name)
        self.setName(name)

    def get_name(self) -> str:
        return self.name().data().decode()

    def set_value(self, value: datatypes.ByteArrayType):
        if isinstance(value, str):
            value = value.encode()
        if isinstance(value, bytes):
            value = QtCore.QByteArray(value)
        self.setValue(value)

    def get_value(self) -> str:
        return self.value().data().decode()

    def set_expiration_date(self, date: datatypes.DateTimeType | None):
        match date:
            case None:
                date = QtCore.QDateTime()
            case str():
                date = dateutil.parser.parse(date)
            case datatypes.DateTimeType():
                pass
            case _:
                raise TypeError(date)
        self.setExpirationDate(date)  # type: ignore


if __name__ == "__main__":
    cookie = NetworkCookie()
