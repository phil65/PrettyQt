from __future__ import annotations

from prettyqt.qt import QtWidgets


class StyleOption(QtWidgets.QStyleOption):
    @classmethod
    def based_on(cls, widget: QtWidgets.QWidget) -> StyleOption:
        opt = cls()
        opt.initFrom(widget)
        return opt
