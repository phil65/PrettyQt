from __future__ import annotations

from typing_extensions import Self

from prettyqt.qt import QtCore


class Time(QtCore.QTime):
    def __repr__(self):
        template = super().__repr__().split("(")[1]  # type: ignore
        return f"{type(self).__name__}({template}"

    def __str__(self):
        return self.toString()

    def __reduce__(self):
        return type(self), (self.hour(), self.minute(), self.second(), self.msec())

    def __format__(self, format_spec: str):
        return self.toString(format_spec)

    @property
    def _hour(self):
        return self.hour()

    @property
    def _minute(self):
        return self.minute()

    @property
    def _second(self):
        return self.second()

    @property
    def _msec(self):
        return self.msec()

    __match_args__ = ("_hour", "_minute", "_second", "_msec")

    def add_msecs(self, msecs: int) -> Self:
        return type(self)(self.addMSecs(msecs))

    def add_secs(self, secs: int) -> Self:
        return type(self)(self.addSecs(secs))

    @classmethod
    def get_current_time(cls) -> Self:
        return cls(cls.currentTime())


if __name__ == "__main__":
    time = Time(22, 1)
