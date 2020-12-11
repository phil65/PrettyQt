from qtpy import QtGui

from prettyqt import gui


QtGui.QDoubleValidator.__bases__ = (gui.Validator,)


class DoubleValidator(QtGui.QDoubleValidator):
    def __repr__(self):
        return f"DoubleValidator({self.bottom()}, {self.top()}, {self.decimals()})"

    def __getstate__(self):
        return dict(bottom=self.bottom(), top=self.top(), decimals=self.decimals())

    def __setstate__(self, state):
        self.__init__(state["bottom"], state["top"], state["decimals"])

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return False
        return (
            self.bottom() == other.bottom()
            and self.top() == other.top()
            and self.decimals() == other.decimals()
        )


if __name__ == "__main__":
    val = DoubleValidator()
    val.setRange(0, 9)
