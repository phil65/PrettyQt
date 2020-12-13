from qtpy import QtCore


class RegExp(QtCore.QRegExp):
    def __repr__(self):
        return f"{type(self).__name__}({self.pattern()!r})"

    def __reduce__(self):
        return self.__class__, (self.pattern(),)


if __name__ == "__main__":
    reg = RegExp()
    reg.setPattern("[0-9]")
