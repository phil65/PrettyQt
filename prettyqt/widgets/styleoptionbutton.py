from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import bidict


BUTTON_FEATURES = bidict(
    none=widgets.QStyleOptionButton.ButtonFeature.None_,
    flat=widgets.QStyleOptionButton.ButtonFeature.Flat,
    has_menu=widgets.QStyleOptionButton.ButtonFeature.HasMenu,
    default_button=widgets.QStyleOptionButton.ButtonFeature.DefaultButton,
    auto_default_button=widgets.QStyleOptionButton.ButtonFeature.AutoDefaultButton,
    command_link_button=widgets.QStyleOptionButton.ButtonFeature.CommandLinkButton,
)


class StyleOptionButton(widgets.StyleOptionMixin, widgets.QStyleOptionButton):
    pass
