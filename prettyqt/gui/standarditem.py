from __future__ import annotations

from collections.abc import Iterator
import html
import os
from typing import Any

from typing_extensions import Self

from prettyqt import constants, core, gui, iconprovider
from prettyqt.utils import datatypes, get_repr, helpers, listdelegators, serializemixin


class StandardItem(serializemixin.SerializeMixin, gui.QStandardItem):
    def __repr__(self):
        return get_repr(self, self.get_icon(), self.text())

    def __getitem__(
        self, index: int | slice | tuple[int | slice, int | slice] | core.QModelIndex
    ) -> gui.QStandardItem | listdelegators.BaseListDelegator[gui.QStandardItem]:
        match index:
            case int():
                if index >= self.childCount():
                    raise IndexError(index)
                return self.child(index)
            case slice():
                return self.__getitem__(index, 0)
            case int() as row, int() as col:
                return self.child(row, col)
            case (row, col):
                rowcount = self.rowCount()
                colcount = self.columnCount()
                children = [
                    self.child(i, j)
                    for i, j in helpers.yield_positions(row, col, rowcount, colcount)
                ]
                return listdelegators.BaseListDelegator(children)
            case _:
                raise TypeError(index)

    def __delitem__(self, index: int | tuple[int, int]):
        item = self.takeRow(index) if isinstance(index, int) else self.takeChild(*index)
        if item is None:
            raise KeyError(index)
        return item

    def __iter__(self) -> Iterator[gui.QStandardItem]:
        return iter(self.get_children())

    def __add__(self, other: str | gui.QStandardItem) -> StandardItem:
        match other:
            case gui.QStandardItem() | str():
                self.add(other)
                return self
            case _:
                raise TypeError("wrong type for addition")

    def get_children(self) -> listdelegators.BaseListDelegator[gui.QStandardItem]:
        items = [self.child(index) for index in range(self.rowCount())]
        return listdelegators.BaseListDelegator(items)

    def add(self, *item: str | gui.QStandardItem):
        for i in item:
            new_item = type(self)(i) if isinstance(i, str) else i
            self.appendRow([new_item])

    def clone(self) -> Self:
        item = type(self)()
        core.DataStream.copy_data(self, item)
        return item

    def set_icon(self, icon: datatypes.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def set_checkstate(
        self, state: constants.CheckStateStr | constants.CheckState | bool
    ):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use
        """
        if isinstance(state, bool):
            state = (
                constants.CheckState.Checked if state else constants.CheckState.Unchecked
            )
        self.setCheckState(constants.CHECK_STATE.get_enum_value(state))

    def is_checked(self):
        return self.checkState() == constants.CheckState.Checked

    def toggle_checkstate(self):
        if self.checkState() == constants.CheckState.Checked:
            self.setCheckState(constants.CheckState.Unchecked)
        else:
            self.setCheckState(constants.CheckState.Checked)

    def get_checkstate(self) -> constants.CheckStateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return constants.CHECK_STATE.inverse[self.checkState()]

    def set_text_alignment(
        self, alignment: constants.AlignmentStr | constants.AlignmentFlag
    ):
        """Set the alignment of the text.

        Args:
            alignment: alignment for the format
        """
        self.setTextAlignment(constants.ALIGNMENTS.get_enum_value(alignment))

    def get_text_alignment(self) -> constants.AlignmentStr:
        """Return current text alignment.

        Returns:
            alignment
        """
        return constants.ALIGNMENTS.inverse[self.textAlignment()]

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def get_foreground(self) -> gui.Brush:
        return gui.Brush(self.foreground())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

    def set_data(self, data: Any, role: constants.ItemDataRoleStr | int):
        item_role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        super().setData(data, item_role)

    def get_data(self, role: constants.ItemDataRoleStr | int):
        item_role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        return super().data(item_role)

    def set_tooltip(
        self,
        tooltip: str | datatypes.PathType,
        size: datatypes.SizeType | None = None,
        rich_text: bool = False,
    ):
        if isinstance(tooltip, os.PathLike):
            path = os.fspath(tooltip)
            if size is None:
                tooltip = f"<img src={path!r}>"
            else:
                if isinstance(size, core.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        if rich_text:
            tooltip = f"<html>{html.escape(tooltip)}</html>"
        super().setToolTip(tooltip)

    def set_size_hint(self, hint: datatypes.SizeType):
        self.setSizeHint(datatypes.to_size(hint))

    def add_item(
        self,
        name: str = "",
        icon: datatypes.IconType = None,
        data: dict | None = None,
        foreground: gui.QBrush | None = None,
        background: gui.QBrush | None = None,
        font: gui.QFont | None = None,
        selectable: bool = True,
        enabled: bool = True,
        editable: bool = False,
        status_tip: str = "",
        tool_tip: str = "",
        whats_this: str | None = None,
        # text_alignment: Optional[str] = None,
        checkstate: constants.CheckStateStr | None = None,
        flags: constants.ItemFlag | None = None,
        size_hint: datatypes.SizeType | None = None,
        is_user_type: bool = False,
    ) -> Self:
        item = type(self)(name)
        if icon is not None:
            icon = iconprovider.get_icon(icon)
            item.setIcon(icon)
        if data is not None:
            for k, v in data.items():
                item.set_data(v, k)
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
    item.set_data("test", 1000)
    item2 = StandardItem()
    item.add(item2)
    print(item.child(0))
