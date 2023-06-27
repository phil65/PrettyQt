from __future__ import annotations

from prettyqt import core, iconprovider, widgets
from prettyqt.qt import QtGui
from prettyqt.utils import datatypes


class IconWidget(widgets.Label):
    def __init__(self, *names, parent: widgets.QWidget | None = None, **kwargs):
        super().__init__(parent=parent)
        self._icon: QtGui.QIcon | None = None
        self._size = core.Size(16, 16)
        self.set_icon(iconprovider._icon(*names, **kwargs))

    def set_icon(self, _icon: datatypes.IconType):
        """Set a new icon().

        Parameters
        ----------
        _icon: qtawesome.icon
            icon to set
        """
        self._icon = iconprovider.get_icon(_icon)
        self.setPixmap(self._icon.pixmap(self._size))

    def set_icon_size(self, size: datatypes.SizeType):
        self._size = datatypes.to_size(size)
        self.update()

    def update(self, *args, **kwargs):
        if self._icon:
            self.setPixmap(self._icon.pixmap(self._size))
        return super().update(*args, **kwargs)


if __name__ == "__main__":
    app = widgets.app()
    widget = IconWidget()
    widget.show()
    bool(widget)
    app.exec()
