# -*- coding: utf-8 -*-

from qtpy import QtNetwork

from prettyqt.utils import bidict

RAW_FORMS = bidict(
    name_and_value_only=QtNetwork.QNetworkCookie.NameAndValueOnly,
    full=QtNetwork.QNetworkCookie.Full,
)


class NetworkCookie(QtNetwork.QNetworkCookie):
    def __repr__(self):
        return "NetworkCookie()"

    def to_raw_form(self, full: bool = True):
        form = RAW_FORMS["full"] if full else RAW_FORMS["name_and_value_only"]
        self.toRawForm(form)

    def set_name(self, name: str):
        self.setName(str.encode(name))

    def get_name(self) -> str:
        return bytes(self.name()).decode()

    def set_value(self, value: str):
        self.setValue(str.encode(value))

    def get_value(self) -> str:
        return bytes(self.value()).decode()
