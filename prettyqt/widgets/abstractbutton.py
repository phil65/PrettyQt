from __future__ import annotations

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import datatypes


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

    def set_style_icon(
        self,
        icon: widgets.style.StandardPixmapStr | widgets.QStyle.StandardPixmap,
        size: datatypes.SizeType,
    ):
        """Set theme icon for the button.

        Args:
            icon: icon to use
            size: icon size
        """
        qicon = self.style().standardIcon(
            widgets.style.STANDARD_PIXMAP.get_enum_value(icon), None, self
        )
        self.set_icon(qicon)
        self.setIconSize(datatypes.to_size(size))

    def set_shortcut(self, shortcut: datatypes.KeySequenceType):
        self.setShortcut(datatypes.to_keysequence(shortcut))

    def get_shortcut(self) -> gui.KeySequence:
        return gui.KeySequence(
            self.shortcut().toString(), gui.KeySequence.SequenceFormat.PortableText
        )

    def setText(self, text: str):
        if not self.objectName() and widgets.app().is_debug():
            self.setObjectName(text)
        super().setText(text)

    def set_icon_size(self, size: datatypes.SizeType):
        """Set size of the icon."""
        self.setIconSize(datatypes.to_size(size))

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: bool):
        self.setChecked(value)

    # def _color(self):
    #     return self.palette().color(QtGui.QPalette.ColorRole.ButtonText)

    # def _set_color(self, qcolor: QtGui.QColor):
    #     palette = self.palette()
    #     palette.setColor(QtGui.QPalette.ColorRole.ButtonText, qcolor)
    #     self.setPalette(palette)

    # color = core.Property(QtGui.QColor, _color, _set_color)

    # @core.Property(QtGui.QColor)
    # def background_color(self):
    #     return self.palette().color(QtGui.QPalette.ColorRole.Button)

    # @background_color.setter
    # def background_color(self, qcolor: QtGui.QColor):
    #     palette = self.palette()
    #     palette.setColor(QtGui.QPalette.ColorRole.Button, qcolor)
    #     self.setPalette(palette)


class AbstractButton(AbstractButtonMixin, QtWidgets.QAbstractButton):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractButton()
    widget.show()
    app.exec()
