from __future__ import annotations

from typing import Self

from prettyqt.qt import QtWidgets


class StyleOptionMixin:
    @classmethod
    def based_on(cls, widget: QtWidgets.QWidget) -> Self:
        opt = cls()
        opt.initFrom(widget)
        return opt


class StyleOption(StyleOptionMixin, QtWidgets.QStyleOption):
    pass
