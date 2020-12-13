from qtpy import QtCore


class Time(QtCore.QTime):
    def __repr__(self):
        template = super().__repr__().split("(")[1]
        return f"{type(self).__name__}({template}"

    def __str__(self):
        return self.toString()

    def __reduce__(self):
        return self.__class__, (self.hour(), self.minute(), self.second(), self.msec())


if __name__ == "__main__":
    time = Time(22, 1)
    print(repr(time))
