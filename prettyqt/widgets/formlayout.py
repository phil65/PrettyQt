from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from prettyqt import constants, widgets
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from collections.abc import Iterator


mod = widgets.QFormLayout

ItemRoleStr = Literal["left", "right", "both"]

ITEM_ROLE: bidict[ItemRoleStr, mod.ItemRole] = bidict(
    left=mod.ItemRole.LabelRole,
    right=mod.ItemRole.FieldRole,
    both=mod.ItemRole.SpanningRole,
)

RowWrapPolicyStr = Literal["dont_wrap", "wrap_long", "wrap_all"]

ROW_WRAP_POLICY: bidict[RowWrapPolicyStr, mod.RowWrapPolicy] = bidict(
    dont_wrap=mod.RowWrapPolicy.DontWrapRows,
    wrap_long=mod.RowWrapPolicy.WrapLongRows,
    wrap_all=mod.RowWrapPolicy.WrapAllRows,
)

FieldGrowthPolicyStr = Literal[
    "fields_stay_at_size", "expanding_fields_grow", "all_non_fixed_fields_grow"
]

FIELD_GROWTH_POLICY: bidict[FieldGrowthPolicyStr, mod.FieldGrowthPolicy] = bidict(
    fields_stay_at_size=mod.FieldGrowthPolicy.FieldsStayAtSizeHint,
    expanding_fields_grow=mod.FieldGrowthPolicy.ExpandingFieldsGrow,
    all_non_fixed_fields_grow=mod.FieldGrowthPolicy.AllNonFixedFieldsGrow,
)


class FormLayout(widgets.LayoutMixin, widgets.QFormLayout):
    """Manages forms of input widgets and their associated labels."""

    ID = "form"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_constraint("maximum")
        self.setVerticalSpacing(8)

    def __setitem__(
        self, index: int | tuple[int, ItemRoleStr], value: str | widgets.QWidget
    ):
        match index:
            case (int() as row, str() as role):
                self.set_widget(value, row, role)
            case int() as row:
                self.set_widget(value, row, "both")
            case _:
                raise TypeError(index)

    def __delitem__(self, index: int):
        self.removeRow(index)

    def __iter__(self) -> Iterator[widgets.QWidget | widgets.QLayout]:
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __len__(self) -> int:
        """Needed for PySide2."""
        return self.rowCount()

    def __add__(self, other: widgets.QWidget | widgets.QLayout | tuple):
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

    def set_form_alignment(
        self, alignment: constants.AlignmentStr | constants.AlignmentFlag
    ):
        """Set the alignment of the form.

        Args:
            alignment: alignment for the form
        """
        self.setFormAlignment(constants.ALIGNMENTS.get_enum_value(alignment))

    def get_form_alignment(self) -> constants.AlignmentStr:
        """Return current form alignment.

        Returns:
            form alignment
        """
        return constants.ALIGNMENTS.inverse[self.formAlignment()]

    def set_label_alignment(
        self, alignment: constants.AlignmentStr | constants.AlignmentFlag
    ):
        """Set the alignment of the label.

        Args:
            alignment: alignment for the label
        """
        self.setFormAlignment(constants.ALIGNMENTS.get_enum_value(alignment))

    def get_label_alignment(self) -> constants.AlignmentStr:
        """Return current label alignment.

        Returns:
            label alignment
        """
        return constants.ALIGNMENTS.inverse[self.labelAlignment()]

    def set_widget(
        self,
        widget: str | widgets.QWidget,
        row: int,
        role: ItemRoleStr | mod.ItemRole = "both",
    ):
        widget = widgets.Label(widget) if isinstance(widget, str) else widget
        self.setWidget(row, ITEM_ROLE.get_enum_value(role), widget)

    def get_widget(
        self, row: int, role: ItemRoleStr | mod.ItemRole = "both"
    ) -> widgets.QLayout | widgets.QWidget:
        item = self.itemAt(row, ITEM_ROLE.get_enum_value(role))
        return i if (i := item.widget()) is not None else item.layout()

    def get_item_position(self, index: int) -> tuple[int, ItemRoleStr] | None:
        row, role = self.getItemPosition(index)  # type: ignore
        return None if row == -1 else (row, ITEM_ROLE.inverse[role])

    def add(self, *items):
        for i in items:
            match i:
                case widgets.QWidget() | widgets.QLayout():
                    self.addRow(i)
                case tuple():
                    self.addRow(*i)
                case _:
                    raise TypeError(i)

    def set_row_wrap_policy(self, policy: RowWrapPolicyStr | mod.RowWrapPolicy):
        """Set row wrap policy to use.

        Args:
            policy: row wrap policy to use
        """
        self.setRowWrapPolicy(ROW_WRAP_POLICY.get_enum_value(policy))

    def get_row_wrap_policy(self) -> RowWrapPolicyStr:
        """Return current row wrap policy.

        Returns:
            row wrap policy
        """
        return ROW_WRAP_POLICY.inverse[self.rowWrapPolicy()]

    def set_field_growth_policy(
        self, policy: FieldGrowthPolicyStr | mod.FieldGrowthPolicy
    ):
        """Set field growth policy to use.

        Args:
            policy: field growth policy to use
        """
        self.setFieldGrowthPolicy(FIELD_GROWTH_POLICY.get_enum_value(policy))

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
    app.exec()
