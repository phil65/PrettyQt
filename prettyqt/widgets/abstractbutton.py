from typing import Tuple, Union

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import InvalidParamError


QtWidgets.QAbstractButton.__bases__ = (widgets.Widget,)


class AbstractButton(QtWidgets.QAbstractButton):
    def serialize_fields(self):
        return dict(
            text=self.text(),
            icon=self.get_icon() if not self.icon().isNull() else None,
            checkable=self.isCheckable(),
            checked=self.isChecked(),
        )

    def __setstate__(self, state):
        self.setText(state["text"])
        self.set_id(state.get("object_name", ""))
        self.set_icon(state["icon"])
        self.setEnabled(state.get("enabled", True))
        self.setChecked(state.get("checked", False))
        self.setCheckable(state["checkable"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_icon(self, icon: gui.icon.IconType):
        """Set the icon for the button.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

    def get_icon(self) -> gui.Icon:
        return gui.Icon(self.icon())

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

    def set_shortcut(self, shortcut: Union[None, QtGui.QKeySequence, str]):
        if shortcut is None:
            shortcut = ""
        self.setShortcut(shortcut)

    def get_shortcut(self) -> gui.KeySequence:
        return gui.KeySequence(self.shortcut())

    def set_text(self, text: str):
        self.setText(text)

    def set_icon_size(self, size: Union[int, Tuple[int, int], QtCore.QSize]):
        """Set size of the icon."""
        if isinstance(size, int):
            size = core.Size(size, size)
        elif isinstance(size, tuple):
            size = core.Size(*size)
        self.setIconSize(size)

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractButton()
    widget.show()
    app.main_loop()
