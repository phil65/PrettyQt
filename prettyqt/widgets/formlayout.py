from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from prettyqt import constants, widgets
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


class FormLayout(widgets.LayoutMixin, QtWidgets.QFormLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_constraint("maximum")
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

    def __iter__(self) -> Iterator[QtWidgets.QWidget | QtWidgets.QLayout]:
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __len__(self) -> int:
        """Needed for PySide2."""
        return self.rowCount()

    def __add__(self, other: QtWidgets.QWidget | QtWidgets.QLayout | tuple):
        self.add(other)
        return self

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "FieldGrowthPolicy": FIELD_GROWTH_POLICY,
            "formAlignment": constants.ALIGNMENTS,
            "labelAlignment": constants.ALIGNMENTS,
            "rowWrapPolicy": ROW_WRAP_POLICY,
        }
        return maps

    def set_form_alignment(self, alignment: constants.AlignmentStr):
        """Set the alignment of the form.

        Args:
            alignment: alignment for the form

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        self.setFormAlignment(constants.ALIGNMENTS[alignment])

    def get_form_alignment(self) -> constants.AlignmentStr:
        """Return current form alignment.

        Returns:
            form alignment
        """
        return constants.ALIGNMENTS.inverse[self.formAlignment()]

    def set_label_alignment(self, alignment: constants.AlignmentStr):
        """Set the alignment of the label.

        Args:
            alignment: alignment for the label

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        self.setFormAlignment(constants.ALIGNMENTS[alignment])

    def get_label_alignment(self) -> constants.AlignmentStr:
        """Return current label alignment.

        Returns:
            label alignment
        """
        return constants.ALIGNMENTS.inverse[self.labelAlignment()]

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
        return None if pos[0] == -1 else (pos[0], ROLE.inverse[pos[1]])

    def add(self, *items):
        for i in items:
            if isinstance(i, QtWidgets.QWidget | QtWidgets.QLayout):
                self.addRow(i)
            elif isinstance(i, tuple):
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
    layout = FormLayout()
    layout[3] = "hellooo"
    w = widgets.Widget()
    w.set_layout(layout)
    w.show()
    app.main_loop()
