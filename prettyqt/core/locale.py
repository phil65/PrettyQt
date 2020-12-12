from qtpy import QtCore


class Locale(QtCore.QLocale):
    def __repr__(self):
        return f"{type(self).__name__}({self.bcp47Name()!r})"

    def __reduce__(self):
        return (self.__class__, (self.bcp47Name(),))


if __name__ == "__main__":
    locale = Locale()
    print(repr(locale))
