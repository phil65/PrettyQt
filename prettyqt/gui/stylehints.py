from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtGui


class StyleHintsMixin(core.ObjectMixin):
    def get_color_scheme(self) -> constants.ColorSchemeStr:
        """Return current color scheme of the system.

        Returns:
            color scheme
        """
        return constants.COLOR_SCHEME.inverse[self.colorScheme()]

    def get_tab_focus_behavior(self) -> constants.TabFocusBehaviorStr:
        """Return current focus behavior on press of the tab key.

        Returns:
            focus behavior
        """
        return constants.TAB_FOCUS_BEHAVIOR.inverse[self.tabFocusBehavior()]


class StyleHintsType(type):
    def __getattr__(self, key):
        return getattr(QtGui.QStyleHints, key)


class StyleHints(StyleHintsMixin, metaclass=StyleHintsType):
    def __init__(self, item: QtGui.QStyleHints):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    hints = StyleHints(app.styleHints())
    scheme = hints.get_color_scheme()
    print(scheme)
