from __future__ import annotations

from typing_extensions import Self

from prettyqt import core


class Time(core.QTime):
    """Clock time functions."""

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
    def _hour(self) -> int:
        return self.hour()

    @property
    def _minute(self) -> int:
        return self.minute()

    @property
    def _second(self) -> int:
        return self.second()

    @property
    def _msec(self) -> int:
        return self.msec()

    __match_args__ = ("_hour", "_minute", "_second", "_msec")

    def add_msecs(self, msecs: int) -> Self:
        return type(self)(self.addMSecs(msecs))

    def add_secs(self, secs: int) -> Self:
        return type(self)(self.addSecs(secs))

    @classmethod
    def get_current_time(cls) -> Self:
        return cls(cls.currentTime())

    @classmethod
    def from_string(cls, *args, **kwargs) -> Self:
        return cls(cls.fromString(*args, **kwargs))


if __name__ == "__main__":
    import datetime

    time = Time(datetime.time(10, 10, 10))
    print(time)
