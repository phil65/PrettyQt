from __future__ import annotations

from prettyqt.qt import QtCore


class Time(QtCore.QTime):
    def __repr__(self):
        template = super().__repr__().split("(")[1]  # type: ignore
        return f"{type(self).__name__}({template}"

    def __str__(self):
        return self.toString()

    def __reduce__(self):
        return type(self), (self.hour(), self.minute(), self.second(), self.msec())

    def add_msecs(self, msecs: int) -> Time:
        return Time(self.addMSecs(msecs))

    def add_secs(self, secs: int) -> Time:
        return Time(self.addSecs(secs))

    @classmethod
    def get_current_time(cls) -> Time:
        return Time(cls.currentTime())


if __name__ == "__main__":
    time = Time(22, 1)
    print(repr(time))
