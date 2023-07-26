from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtHelp


class HelpFilterSettingsWidget(widgets.WidgetMixin, QtHelp.QHelpFilterSettingsWidget):
    """Widget that allows for creating, editing and removing filters."""


if __name__ == "__main__":
    app = widgets.app()
    widget = HelpFilterSettingsWidget()
    widget.show()
    app.exec()
