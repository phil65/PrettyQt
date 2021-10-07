from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


mod = QtWidgets.QFormLayout

ROLE = bidict(
    left=mod.ItemRole.LabelRole,
    right=mod.ItemRole.FieldRole,
    both=mod.ItemRole.SpanningRole,
)

RoleStr = Literal["left", "right", "both"]

ROW_WRAP_POLICY = bidict(
    dont_wrap=mod.RowWrapPolicy.DontWrapRows,
    wrap_long=mod.RowWrapPolicy.WrapLongRows,
    wrap_all=mod.RowWrapPolicy.WrapAllRows,
)

RowWrapPolicyStr = Literal["dont_wrap", "wrap_long", "wrap_all"]

FIELD_GROWTH_POLICY = bidict(
    fields_stay_at_size=mod.FieldGrowthPolicy.FieldsStayAtSizeHint,
    expanding_fields_grow=mod.FieldGrowthPolicy.ExpandingFieldsGrow,
    all_non_fixed_fields_grow=mod.FieldGrowthPolicy.AllNonFixedFieldsGrow,
)

FieldGrowthPolicyStr = Literal[
    "fields_stay_at_size", "expanding_fields_grow", "all_non_fixed_fields_grow"
]

QtWidgets.QFormLayout.__bases__ = (widgets.Layout,)


class FormLayout(QtWidgets.QFormLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_mode("maximum")
        self.setVerticalSpacing(8)

    def __setitem__(
        self, index: int | tuple[int, RoleStr], value: str | QtWidgets.QWidget
    ):
        if isinstance(index, tuple):
            row = index[0]
            role = index[1]
        else:
            row = index
            role = "both"
        self.set_widget(value, row, role)

    def __delitem__(self, index: int):
        self.removeRow(index)

    def __iter__(self):
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __len__(self) -> int:
        """Needed for PySide2."""
        return self.rowCount()

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout | tuple):
        self.add(other)
        return self

    def serialize_fields(self):
        widget_list = []
        positions = []
        for i, item in enumerate(list(self)):
            widget_list.append(item)
            positions.append(self.get_item_position(i))
        return dict(widgets=widget_list, positions=positions)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __setstate__(self, state):
        for i, (item, pos) in enumerate(zip(state["widgets"], state["positions"])):
            self.set_widget(item, pos[0], pos[1])

    def set_widget(
        self, widget: str | QtWidgets.QWidget, row: int, role: RoleStr = "both"
    ):
        if isinstance(widget, str):
            widget = widgets.Label(widget)
        self.setWidget(row, ROLE[role], widget)

    def get_widget(
        self, row: int, role: RoleStr = "both"
    ) -> QtWidgets.QLayout | QtWidgets.QWidget:
        item = self.itemAt(row, ROLE[role])
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

    def get_item_position(self, index: int) -> tuple[int, RoleStr] | None:
        pos = self.getItemPosition(index)  # type: ignore
        if pos[0] == -1:  # type: ignore
            return None
        return pos[0], ROLE.inverse[pos[1]]  # type: ignore

    def add(self, *items):
        for i in items:
            if isinstance(i, (QtWidgets.QWidget, QtWidgets.QLayout)):
                self.addRow(i)
            if isinstance(i, tuple):
                self.addRow(*i)

    def set_row_wrap_policy(self, policy: RowWrapPolicyStr):
        """Set row wrap policy to use.

        Args:
            policy: row wrap policy to use

        Raises:
            InvalidParamError: row wrap policy does not exist
        """
        if policy not in ROW_WRAP_POLICY:
            raise InvalidParamError(policy, ROW_WRAP_POLICY)
        self.setRowWrapPolicy(ROW_WRAP_POLICY[policy])

    def get_row_wrap_policy(self) -> RowWrapPolicyStr:
        """Return current row wrap policy.

        Returns:
            row wrap policy
        """
        return ROW_WRAP_POLICY.inverse[self.rowWrapPolicy()]

    def set_field_growth_policy(self, policy: FieldGrowthPolicyStr):
        """Set field growth policy to use.

        Args:
            policy: field growth policy to use

        Raises:
            InvalidParamError: field growth policy does not exist
        """
        if policy not in FIELD_GROWTH_POLICY:
            raise InvalidParamError(policy, FIELD_GROWTH_POLICY)
        self.setFieldGrowthPolicy(FIELD_GROWTH_POLICY[policy])

    def get_field_growth_policy(self) -> FieldGrowthPolicyStr:
        """Return current field growth policy.

        Returns:
            field growth policy
        """
        return FIELD_GROWTH_POLICY.inverse[self.fieldGrowthPolicy()]


if __name__ == "__main__":
    app = widgets.app()
    dct = {"key": widgets.Label("test"), None: widgets.Label("test 2")}
    layout = FormLayout.build_from_dict(dct)
    layout[3] = "hellooo"
    w = widgets.Widget()
    w.set_layout(layout)
    w.show()
    app.main_loop()
