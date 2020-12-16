from typing import Any, Dict, Literal

from qtpy import QtWidgets

from prettyqt.utils import InvalidParamError, bidict, helpers, prettyprinter


SIZE_POLICY = bidict(
    fixed=QtWidgets.QSizePolicy.Fixed,
    minimum=QtWidgets.QSizePolicy.Minimum,
    maximum=QtWidgets.QSizePolicy.Maximum,
    preferred=QtWidgets.QSizePolicy.Preferred,
    expanding=QtWidgets.QSizePolicy.Expanding,
    minimum_expanding=QtWidgets.QSizePolicy.MinimumExpanding,
    ignored=QtWidgets.QSizePolicy.Ignored,
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
    default=QtWidgets.QSizePolicy.DefaultType,
    buttonbox=QtWidgets.QSizePolicy.ButtonBox,
    checkbox=QtWidgets.QSizePolicy.CheckBox,
    combobox=QtWidgets.QSizePolicy.ComboBox,
    frame=QtWidgets.QSizePolicy.Frame,
    groupbox=QtWidgets.QSizePolicy.GroupBox,
    label=QtWidgets.QSizePolicy.Label,
    line=QtWidgets.QSizePolicy.Line,
    lineedit=QtWidgets.QSizePolicy.LineEdit,
    pushbutton=QtWidgets.QSizePolicy.PushButton,
    radiobutton=QtWidgets.QSizePolicy.RadioButton,
    slider=QtWidgets.QSizePolicy.Slider,
    spinbox=QtWidgets.QSizePolicy.SpinBox,
    tabwidget=QtWidgets.QSizePolicy.TabWidget,
    toolbutton=QtWidgets.QSizePolicy.ToolButton,
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
        cls_name = self.__class__.__name__
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
        )

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.setHeightForWidth(state["has_height_for_width"])
        self.setWidthForHeight(state["has_width_for_height"])
        self.setHorizontalStretch(state["horizontal_stretch"])
        self.setVerticalStretch(state["vertical_stretch"])
        self.set_horizontal_policy(state["horizontal_policy"])
        self.set_vertical_policy(state["vertical_policy"])
        self.setRetainSizeWhenHidden(state["retain_size_when_hidden"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize(self):
        return self.__getstate__()

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
