from __future__ import annotations

from typing import Any, Literal

from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict, helpers, prettyprinter


SIZE_POLICY = bidict(
    fixed=QtWidgets.QSizePolicy.Policy.Fixed,
    minimum=QtWidgets.QSizePolicy.Policy.Minimum,
    maximum=QtWidgets.QSizePolicy.Policy.Maximum,
    preferred=QtWidgets.QSizePolicy.Policy.Preferred,
    expanding=QtWidgets.QSizePolicy.Policy.Expanding,
    minimum_expanding=QtWidgets.QSizePolicy.Policy.MinimumExpanding,
    ignored=QtWidgets.QSizePolicy.Policy.Ignored,
)

SizePolicyStr = Literal[
    "fixed",
    "minimum",
    "maximum",
    "preferred",
    "expanding",
    "minimum_expanding",
    "ignored",
]

CONTROL_TYPE = bidict(
    default=QtWidgets.QSizePolicy.ControlType.DefaultType,
    buttonbox=QtWidgets.QSizePolicy.ControlType.ButtonBox,
    checkbox=QtWidgets.QSizePolicy.ControlType.CheckBox,
    combobox=QtWidgets.QSizePolicy.ControlType.ComboBox,
    frame=QtWidgets.QSizePolicy.ControlType.Frame,
    groupbox=QtWidgets.QSizePolicy.ControlType.GroupBox,
    label=QtWidgets.QSizePolicy.ControlType.Label,
    line=QtWidgets.QSizePolicy.ControlType.Line,
    lineedit=QtWidgets.QSizePolicy.ControlType.LineEdit,
    pushbutton=QtWidgets.QSizePolicy.ControlType.PushButton,
    radiobutton=QtWidgets.QSizePolicy.ControlType.RadioButton,
    slider=QtWidgets.QSizePolicy.ControlType.Slider,
    spinbox=QtWidgets.QSizePolicy.ControlType.SpinBox,
    tabwidget=QtWidgets.QSizePolicy.ControlType.TabWidget,
    toolbutton=QtWidgets.QSizePolicy.ControlType.ToolButton,
)

ControlTypeStr = Literal[
    "default",
    "buttonbox",
    "checkbox",
    "combobox",
    "frame",
    "groupbox",
    "label",
    "line",
    "lineedit",
    "pushbutton",
    "radiobutton",
    "slider",
    "spinbox",
    "tabwidget",
    "toolbutton",
]


class SizePolicy(prettyprinter.PrettyPrinter, QtWidgets.QSizePolicy):
    def __repr__(self) -> str:
        cls_name = type(self).__name__
        params = helpers.format_kwargs(self.__getstate__())
        return f"{cls_name}({params})"

    def __getstate__(self):
        return dict(
            has_height_for_width=self.hasHeightForWidth(),
            has_width_for_height=self.hasWidthForHeight(),
            horizontal_stretch=self.horizontalStretch(),
            vertical_stretch=self.verticalStretch(),
            horizontal_policy=self.get_horizontal_policy(),
            vertical_policy=self.get_vertical_policy(),
            retain_size_when_hidden=self.retainSizeWhenHidden(),
            control_type=self.get_control_type(),
        )

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.setHeightForWidth(state["has_height_for_width"])
        self.setWidthForHeight(state["has_width_for_height"])
        self.setHorizontalStretch(state["horizontal_stretch"])
        self.setVerticalStretch(state["vertical_stretch"])
        self.set_horizontal_policy(state["horizontal_policy"])
        self.set_vertical_policy(state["vertical_policy"])
        self.setRetainSizeWhenHidden(state["retain_size_when_hidden"])
        self.set_control_type(state["control_type"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize(self) -> dict[str, Any]:
        return self.__getstate__()

    @classmethod
    def clone(cls, qpol: QtWidgets.QSizePolicy) -> SizePolicy:
        pol = cls(qpol.horizontalPolicy(), qpol.verticalPolicy(), qpol.controlType())
        pol.setHeightForWidth(qpol.hasHeightForWidth())
        pol.setWidthForHeight(qpol.hasWidthForHeight())
        pol.setHorizontalStretch(qpol.horizontalStretch())
        pol.setVerticalStretch(qpol.verticalStretch())
        pol.setRetainSizeWhenHidden(qpol.retainSizeWhenHidden())
        return pol

    def get_horizontal_policy(self) -> SizePolicyStr:
        """Return size policy.

        Returns:
            horizontal size policy
        """
        return SIZE_POLICY.inverse[self.horizontalPolicy()]

    def set_horizontal_policy(self, policy: SizePolicyStr) -> None:
        """Set the horizontal policy.

        Args:
            policy: policy to set

        Raises:
            InvalidParamError: policy does not exist
        """
        self.setHorizontalPolicy(SIZE_POLICY[policy])

    def get_vertical_policy(self) -> SizePolicyStr:
        """Return size policy.

        Returns:
            vertical size policy

        """
        return SIZE_POLICY.inverse[self.verticalPolicy()]

    def set_vertical_policy(self, policy: SizePolicyStr) -> None:
        """Set the horizontal policy.

        Args:
            policy: policy to set

        Raises:
            InvalidParamError: policy does not exist
        """
        self.setVerticalPolicy(SIZE_POLICY[policy])

    def get_control_type(self) -> ControlTypeStr:
        """Return control type.

        Returns:
            control type
        """
        return CONTROL_TYPE.inverse[self.controlType()]

    def set_control_type(self, typ: ControlTypeStr) -> None:
        """Set the control type.

        Args:
            typ: control type to set

        Raises:
            InvalidParamError: control type does not exist
        """
        if typ not in CONTROL_TYPE:
            raise InvalidParamError(typ, CONTROL_TYPE)
        self.setControlType(CONTROL_TYPE[typ])
