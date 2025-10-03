from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import iconprovider, widgets
from prettyqt.utils import get_repr


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class IconLabel(widgets.Widget):
    def __init__(
        self,
        text: str | None = None,
        tooltip: str = "",
        icon: datatypes.IconType = "mdi.help-circle-outline",
        parent: widgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.set_layout("horizontal", spacing=0)
        self.label = widgets.Label(text, margin=10)
        self.label.set_size_policy(horizontal="minimum")
        icon = iconprovider.get_icon(icon)
        self.icon = widgets.Label(tool_tip=tooltip, pixmap=icon.pixmap(20, 20))
        self.icon.set_size_policy(horizontal="minimum")
        self.box.add(self.label)
        self.box.add(self.icon)
        self.box.addStretch()

    def __getattr__(self, value: str):
        return self.label.__getattribute__(value)

    def __repr__(self):
        return get_repr(self, self.text())


if __name__ == "__main__":
    app = widgets.app()
    widget = IconLabel("test", tooltip="testus")
    widget.show()
    app.exec()
