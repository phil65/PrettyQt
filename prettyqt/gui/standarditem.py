from __future__ import annotations

from collections.abc import Iterator
import os

from prettyqt import constants, core, gui, iconprovider
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, types


class StandardItem(QtGui.QStandardItem):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_icon()}, {self.text()!r})"

    def serialize_fields(self):
        return dict(
            text=self.text(),
            tool_tip=self.toolTip(),
            status_tip=self.statusTip(),
            icon=self.get_icon(),
            data=self.data(),
        )

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    def __getitem__(
        self, index: int | tuple[int, int] | QtCore.QModelIndex
    ) -> QtGui.QStandardItem:
        if isinstance(index, int):
            return self.child(index)
        elif isinstance(index, tuple):
            return self.child(*index)
        else:
            raise KeyError(index)

    def __delitem__(self, index: int | tuple[int, int]):
        if isinstance(index, int):
            item = self.takeRow(index)
        else:
            item = self.takeChild(*index)
        if item is None:
            raise KeyError(index)
        return item

    def __iter__(self) -> Iterator[QtGui.QStandardItem]:
        return iter(self.get_children())

    def __add__(self, other: str | QtGui.QStandardItem) -> StandardItem:
        if isinstance(other, (QtGui.QStandardItem, str)):
            self.add(other)
            return self
        raise TypeError("wrong type for addition")

    def get_children(self) -> list[QtGui.QStandardItem]:
        return [self.child(index) for index in range(self.rowCount())]

    def add(self, *item: str | QtGui.QStandardItem):
        for i in item:
            if isinstance(i, str):
                i = gui.StandardItem(i)
            self.appendRow([i])

    def clone(self):
        item = type(self)()
        core.DataStream.copy_data(self, item)
        assert type(item) == StandardItem
        return item

    def set_icon(self, icon: types.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def set_checkstate(self, state: constants.StateStr):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in constants.STATE:
            raise InvalidParamError(state, constants.STATE)
        self.setCheckState(constants.STATE[state])

    def get_checkstate(self) -> constants.StateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return constants.STATE.inverse[self.checkState()]

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def get_foreground(self) -> gui.Brush:
        return gui.Brush(self.foreground())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        if icon.isNull():
            return None
        return gui.Icon(icon)

    def set_tooltip(
        self,
        tooltip: str | types.PathType,
        size: types.SizeType | None = None,
    ):
        if isinstance(tooltip, os.PathLike):
            path = os.fspath(tooltip)
            if size is None:
                tooltip = f"<img src={path!r}>"
            else:
                if isinstance(size, QtCore.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        self.setToolTip(tooltip)

    def set_size_hint(self, hint: types.SizeType):
        if isinstance(hint, tuple):
            hint = QtCore.QSize(*hint)
        self.setSizeHint(hint)

    def add_item(
        self,
        name: str = "",
        icon: types.IconType = None,
        data: dict | None = None,
        foreground: QtGui.QBrush | None = None,
        background: QtGui.QBrush | None = None,
        font: QtGui.QFont | None = None,
        selectable: bool = True,
        enabled: bool = True,
        editable: bool = False,
        status_tip: str | None = None,
        tool_tip: str | None = None,
        whats_this: str | None = None,
        # text_alignment: Optional[str] = None,
        checkstate: constants.StateStr | None = None,
        flags: QtCore.Qt.ItemFlags | None = None,
        size_hint: types.SizeType | None = None,
        is_user_type: bool = False,
    ) -> StandardItem:
        item = StandardItem(name)
        if icon is not None:
            icon = iconprovider.get_icon(icon)
            item.setIcon(icon)
        if data is not None:
            for k, v in data.items():
                item.setData(v, k)
        if foreground is not None:
            item.setForeground(foreground)
        if background is not None:
            item.setBackground(background)
        if font is not None:
            item.setFont(font)
        if flags is not None:
            item.setFlags(flags)
        if enabled:
            item.setEnabled(enabled)
        if editable:
            item.setEditable(editable)
        if selectable:
            item.setSelectable(selectable)
        if status_tip:
            item.setStatusTip(status_tip)
        if tool_tip:
            item.setToolTip(tool_tip)
        if whats_this:
            item.setWhatsThis(whats_this)
        if size_hint is not None:
            item.set_size_hint(size_hint)
        if checkstate is not None:
            item.set_checkstate(checkstate)
        self.appendRow([item])
        return item


if __name__ == "__main__":
    item = StandardItem()
    item.setData("test", 1000)
    item2 = StandardItem()
    item.add(item2)
    print(item.child(0))
