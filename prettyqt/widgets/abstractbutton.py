from __future__ import annotations

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, datatypes


class AbstractButtonMixin(widgets.WidgetMixin):
    def __bool__(self):
        return self.isChecked()

    def set_icon(self, icon: datatypes.IconType):
        """Set the icon for the button.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

    def set_style_icon(self, icon: widgets.style.StandardPixmapStr, size: int = 15):
        """Set theme icon for the button.

        Args:
            icon: icon to use
            size: icon size
        """
        if icon not in widgets.style.STANDARD_PIXMAP:
            raise InvalidParamError(icon, widgets.style.STANDARD_PIXMAP)
        qicon = self.style().standardIcon(widgets.style.STANDARD_PIXMAP[icon], None, self)
        self.set_icon(qicon)
        self.setIconSize(core.Size(size, size))

    def set_shortcut(self, shortcut: None | QtGui.QKeySequence | str):
        if shortcut is None:
            shortcut = ""
        if isinstance(shortcut, str):
            shortcut = gui.KeySequence(
                shortcut, gui.KeySequence.SequenceFormat.PortableText
            )
        self.setShortcut(shortcut)

    def get_shortcut(self) -> gui.KeySequence:
        return gui.KeySequence(
            self.shortcut().toString(), gui.KeySequence.SequenceFormat.PortableText
        )

    def set_text(self, text: str):
        self.setText(text)

    def set_icon_size(self, size: int | datatypes.SizeType):
        """Set size of the icon."""
        if isinstance(size, int):
            size = core.Size(size, size)
        elif isinstance(size, tuple):
            size = core.Size(*size)
        self.setIconSize(size)

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: bool):
        self.setChecked(value)

    @property
    def is_on(self) -> bool:
        return self.isChecked()

    @is_on.setter
    def is_on(self, state: bool):
        self.setChecked(state)


class AbstractButton(AbstractButtonMixin, QtWidgets.QAbstractButton):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractButton()
    widget.show()
    app.main_loop()
