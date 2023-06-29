from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtNetwork
from prettyqt.utils import bidict, datatypes, get_repr


RawFormStr = Literal["name_and_value_only", "full"]

RAW_FORMS: bidict[RawFormStr, QtNetwork.QNetworkCookie.RawForm] = bidict(
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
        name = datatypes.to_bytearray(name)
        self.setName(name)

    def get_name(self) -> str:
        return self.name().data().decode()

    def set_value(self, value: datatypes.ByteArrayType):
        value = datatypes.to_bytearray(value)
        self.setValue(value)

    def get_value(self) -> str:
        return self.value().data().decode()

    def set_expiration_date(self, date: datatypes.DateTimeType | None):
        date = datatypes.to_datetime(date)
        self.setExpirationDate(date)  # type: ignore


if __name__ == "__main__":
    cookie = NetworkCookie()
