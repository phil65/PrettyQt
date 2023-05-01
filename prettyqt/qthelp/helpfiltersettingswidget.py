from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtHelp


class HelpFilterSettingsWidget(widgets.Widget, QtHelp.QHelpFilterSettingsWidget):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = HelpFilterSettingsWidget()
    widget.show()
    app.main_loop()
