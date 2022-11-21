from __future__ import annotations

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, types


QtWidgets.QAbstractButton.__bases__ = (widgets.Widget,)


class AbstractButton(QtWidgets.QAbstractButton):
    def serialize_fields(self):
        return dict(
            text=self.text(),
            icon=self.get_icon(),
            checkable=self.isCheckable(),
            checked=self.isChecked(),
            auto_exclusive=self.autoExclusive(),
            auto_repeat=self.autoRepeat(),
            auto_repeat_delay=self.autoRepeatDelay(),
            auto_repeat_interval=self.autoRepeatInterval(),
            is_down=self.isDown(),
            icon_size=self.get_icon_size(),
            shortcut=self.get_shortcut(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setText(state["text"])
        self.set_icon(state["icon"])
        self.setChecked(state.get("checked", False))
        self.setCheckable(state["checkable"])
        self.setAutoExclusive(state["auto_exclusive"])
        self.setAutoRepeat(state["auto_repeat"])
        self.setAutoRepeatDelay(state["auto_repeat_delay"])
        self.setAutoRepeatInterval(state["auto_repeat_interval"])
        self.setDown(state["is_down"])
        self.set_icon_size(state["icon_size"])
        self.setShortcut(state["shortcut"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bool__(self):
        return self.isChecked()

    def set_icon(self, icon: types.IconType):
        """Set the icon for the button.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        if icon.isNull():
            return None
        return gui.Icon(icon)

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

    def set_icon_size(self, size: int | types.SizeType):
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


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractButton()
    widget.show()
    app.main_loop()
