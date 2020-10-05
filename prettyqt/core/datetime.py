# -*- coding: utf-8 -*-

import datetime

from qtpy import QtCore

from prettyqt import core


class DateTime(QtCore.QDateTime):
    def __repr__(self):
        template = super().__repr__().split("(")[1]
        return f"DateTime({template}"

    def __str__(self):
        return self.toString("yyyy-MM-dd hh:mm:ss.zzzzzz")

    def __reduce__(self):
        return (self.__class__, (self.date(), self.time()))

    def get_value(self) -> datetime.datetime:
        try:
            return self.toPython()
        except TypeError:
            return self.toPyDateTime()


if __name__ == "__main__":
    date = core.Date(2000, 11, 11)
    dt = DateTime(date)
