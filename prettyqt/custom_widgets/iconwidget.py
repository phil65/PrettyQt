from __future__ import annotations

from prettyqt import core, iconprovider, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import types


class IconWidget(widgets.Label):
    """IconWidget gives the ability to display an icon as a widget.

    if supports the same arguments as icon()
    for example
    music_icon = qta.IconWidget('fa5s.music',
                                color='blue',
                                color_active='orange')

    it also have setIcon() and setIconSize() functions
    """

    def __init__(self, *names, parent: QtWidgets.QWidget | None = None, **kwargs):
        super().__init__(parent=parent)
        self._icon: QtGui.QIcon | None = None
        self._size = core.Size(16, 16)
        self.set_icon(iconprovider._icon(*names, **kwargs))

    def set_icon(self, _icon: types.IconType):
        """Set a new icon().

        Parameters
        ----------
        _icon: qtawesome.icon
            icon to set
        """
        self._icon = iconprovider.get_icon(_icon)
        self.setPixmap(self._icon.pixmap(self._size))

    def set_icon_size(self, size: int | types.SizeType):
        if isinstance(size, tuple):
            size = QtCore.QSize(*size)
        elif isinstance(size, int):
            size = QtCore.QSize(size, size)
        self._size = size
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
    app.main_loop()
