from __future__ import annotations

from prettyqt import iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


class IconLabel(widgets.Widget):
    def __init__(
        self,
        text: str | None = None,
        tooltip: str = "",
        icon: types.IconType = "mdi.help-circle-outline",
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.set_layout("horizontal")
        self.label = widgets.Label(text)
        self.label.setMargin(10)
        self.label.set_size_policy(horizontal="minimum")
        self.tooltip = tooltip
        icon = iconprovider.get_icon(icon)
        self.icon = widgets.Label()
        self.icon.setToolTip(tooltip)
        self.icon.set_size_policy(horizontal="minimum")
        pixmap = icon.pixmap(20, 20)
        self.icon.setPixmap(pixmap)
        self.box.add(self.label)
        self.box.add(self.icon)
        self.box.setSpacing(0)
        self.box.addStretch()

    def __getattr__(self, value: str):
        return self.label.__getattribute__(value)

    def __repr__(self):
        return f"{type(self).__name__}({self.text()!r})"


if __name__ == "__main__":
    app = widgets.app()
    widget = IconLabel("test", tooltip="testus")
    widget.show()
    app.main_loop()
