from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


BUTTON_FEATURES = bidict(
    none=QtWidgets.QStyleOptionButton.ButtonFeature.None_,
    flat=QtWidgets.QStyleOptionButton.ButtonFeature.Flat,
    has_menu=QtWidgets.QStyleOptionButton.ButtonFeature.HasMenu,
    default_button=QtWidgets.QStyleOptionButton.ButtonFeature.DefaultButton,
    auto_default_button=QtWidgets.QStyleOptionButton.ButtonFeature.AutoDefaultButton,
    command_link_button=QtWidgets.QStyleOptionButton.ButtonFeature.CommandLinkButton,
)


QtWidgets.QStyleOptionButton.__bases__ = (widgets.StyleOption,)


class StyleOptionButton(QtWidgets.QStyleOptionButton):
    pass
