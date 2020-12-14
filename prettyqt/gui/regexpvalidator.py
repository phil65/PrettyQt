from qtpy import QtGui

from prettyqt import core, gui


QtGui.QRegExpValidator.__bases__ = (gui.Validator,)


class RegExpValidator(QtGui.QRegExpValidator):
    def __repr__(self):
        return f"{type(self).__name__}(RegExp({self.get_regex()!r}))"

    def __getstate__(self):
        return dict(regexp=core.RegExp(self.regExp()))

    def __setstate__(self, state):
        self.setRegExp(state["regexp"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return False
        return self.regExp() == other.regExp()

    def set_regex(self, regex: str):
        re = core.RegExp(regex)
        self.setRegExp(re)

    def get_regex(self) -> str:
        val = self.regExp()
        return val.pattern()


if __name__ == "__main__":
    val = RegExpValidator()
    val.set_regex(r"\w\d\d")
