# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError, prettyprinter


STYLE_HINTS = bidict(
    any=QtGui.QFont.AnyStyle,
    sans_serif=QtGui.QFont.SansSerif,
    serif=QtGui.QFont.Serif,
    typewriter=QtGui.QFont.TypeWriter,
    decorative=QtGui.QFont.Decorative,
    monospace=QtGui.QFont.Monospace,
    fantasy=QtGui.QFont.Fantasy,
    cursive=QtGui.QFont.Cursive,
    system=QtGui.QFont.System,
)

WEIGHTS = bidict(
    thin=QtGui.QFont.Thin,
    extra_light=QtGui.QFont.ExtraLight,
    light=QtGui.QFont.Light,
    normal=QtGui.QFont.Normal,
    medium=QtGui.QFont.Medium,
    demi_bold=QtGui.QFont.DemiBold,
    bold=QtGui.QFont.Bold,
    extra_bold=QtGui.QFont.ExtraBold,
    black=QtGui.QFont.Black,
)


class Font(prettyprinter.PrettyPrinter, QtGui.QFont):
    def __repr__(self):
        return (
            f"Font('{self.family()}', {self.pointSize()}, "
            f"{self.weight()}, {self.italic()})"
        )

    def __getstate__(self):
        return dict(
            family=self.family(),
            pointsize=self.pointSize(),
            weight=self.weight(),
            italic=self.italic(),
        )

    def serialize(self):
        return self.__getstate__()

    def __setstate__(self, state):
        self.__init__()
        self.setFamily(state["family"])
        if state["pointsize"] > -1:
            self.setPointSize(state["pointsize"])
        self.setWeight(state["weight"])
        self.setItalic(state["italic"])

    @property
    def metrics(self):
        return gui.FontMetrics(self)

    def set_size(self, size: int):
        self.setPointSize(size)

    @classmethod
    def mono(cls, size=8):
        font = cls("Consolas", size)
        # font.setStyleHint()
        return font

    def set_style_hint(self, hint: str):
        """Set the style hint.

        Valid values are "any", "sans_serif", "serif", "typewriter", "decorative",
        "monospace", "fantasy", "cursive", "system"

        Args:
            hint: style hint

        Raises:
            InvalidParamError: invalid style hint
        """
        if hint not in STYLE_HINTS:
            raise InvalidParamError(hint, STYLE_HINTS)
        self.setStyleHint(STYLE_HINTS[hint])

    def set_weight(self, weight: str):
        """Set the font weight.

        Valid values are "thin", "extra_light", light", "medium", "demi_bold", "bold",
                         "extra_bold", normal", "black"

        Args:
            weight: font weight

        Raises:
            InvalidParamError: invalid font weight
        """
        if weight not in WEIGHTS:
            raise InvalidParamError(weight, WEIGHTS)
        self.setWeight(WEIGHTS[weight])


if __name__ == "__main__":
    font = Font("Consolas")
