from typing import Literal, Optional

from qtpy import QtWidgets, QtCore

from prettyqt import gui
from prettyqt.utils import bidict, InvalidParamError

STATE = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)

StateStr = Literal["unchecked", "partial", "checked"]

H_ALIGNMENTS = bidict(
    left=QtCore.Qt.AlignLeft,
    right=QtCore.Qt.AlignRight,
    center=QtCore.Qt.AlignHCenter,
    justify=QtCore.Qt.AlignJustify,
)

HorizontalAlignmentStr = Literal[
    "left",
    "right",
    "center",
    "justify",
]

V_ALIGNMENTS = bidict(
    top=QtCore.Qt.AlignTop,
    bottom=QtCore.Qt.AlignBottom,
    center=QtCore.Qt.AlignVCenter,
    baseline=QtCore.Qt.AlignBaseline,
)

VerticalAlignmentStr = Literal[
    "top",
    "bottom",
    "center",
    "baseline",
]


class TableWidgetItem(QtWidgets.QTableWidgetItem):
    def __setitem__(self, index: int, value):
        self.setData(index, value)

    def __getitem__(self, index: int):
        return self.data(index)

    def serialize_fields(self):
        return dict(
            text=self.text(),
            tool_tip=self.toolTip(),
            status_tip=self.statusTip(),
            checkstate=self.get_checkstate(),
            icon=gui.Icon(self.icon()) if not self.icon().isNull() else None,
            data=self.data(QtCore.Qt.UserRole),
        )

    def set_icon(self, icon: gui.icon.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

    def set_checkstate(self, state: StateStr):
        """Set checkstate of the checkbox.

        Args:
            state: checkstate to use

        Raises:
            InvalidParamError: invalid checkstate
        """
        if state not in STATE:
            raise InvalidParamError(state, STATE)
        self.setCheckState(STATE[state])

    def get_checkstate(self) -> StateStr:
        """Return checkstate.

        Returns:
            checkstate
        """
        return STATE.inverse[self.checkState()]

    def set_text_alignment(
        self,
        horizontal: Optional[HorizontalAlignmentStr] = None,
        vertical: Optional[VerticalAlignmentStr] = None,
    ):
        """Set text alignment of the checkbox.

        Args:
            alignment: text alignment to use

        Raises:
            InvalidParamError: invalid text alignment
        """
        if horizontal is None and vertical is not None:
            flag = V_ALIGNMENTS[vertical]
        elif vertical is None and horizontal is not None:
            flag = H_ALIGNMENTS[horizontal]
        elif vertical is not None and horizontal is not None:
            flag = V_ALIGNMENTS[vertical] | H_ALIGNMENTS[horizontal]
        else:
            return
        self.setTextAlignment(flag)

    def get_background(self) -> gui.Brush:
        return gui.Brush(self.background())

    def get_foreground(self) -> gui.Brush:
        return gui.Brush(self.foreground())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_icon(self) -> gui.Icon:
        return gui.Icon(self.icon())


if __name__ == "__main__":
    item = TableWidgetItem()
