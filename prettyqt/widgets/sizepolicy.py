# -*- coding: utf-8 -*-

from typing import Callable, Any, Generator, Dict
from qtpy import QtWidgets

from prettyqt.utils import bidict, helpers


SIZE_POLICIES = bidict(
    fixed=QtWidgets.QSizePolicy.Fixed,
    minimum=QtWidgets.QSizePolicy.Minimum,
    maximum=QtWidgets.QSizePolicy.Maximum,
    preferred=QtWidgets.QSizePolicy.Preferred,
    expanding=QtWidgets.QSizePolicy.Expanding,
    minimum_expanding=QtWidgets.QSizePolicy.MinimumExpanding,
    ignored=QtWidgets.QSizePolicy.Ignored,
)

CONTROL_TYPES = bidict(
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


class SizePolicy(QtWidgets.QSizePolicy):
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
        super().__init__()
        self.setHeightForWidth(state["has_height_for_width"])
        self.setWidthForHeight(state["has_width_for_height"])
        self.setHorizontalStretch(state["horizontal_stretch"])
        self.setVerticalStretch(state["vertical_stretch"])
        self.set_horizontal_policy(state["horizontal_policy"])
        self.set_vertical_policy(state["vertical_policy"])
        self.setRetainSizeWhenHidden(state["retain_size_when_hidden"])

    def __pretty__(
        self, fmt: Callable[[Any], Any], **kwargs: Any
    ) -> Generator[Any, None, None]:
        """Provide a human readable representations of objects.

        Used by devtools (https://python-devtools.helpmanual.io/).
        """
        yield self.__class__.__name__ + "("
        yield 1
        for k, v in self.__getstate__().items():
            yield f"{k}={v!r}"
            yield 0
        yield -1
        yield ")"

    def get_horizontal_policy(self) -> str:
        """Return size policy.

        possible values are "fixed", "minimum", "maximum", "preferred",
        "expanding", "minimum_expanding" and "ignored"

        Returns:
            horizontal size policy
        """
        return SIZE_POLICIES.inv[self.horizontalPolicy()]

    def set_horizontal_policy(self, mode: str) -> None:
        """Set the horizontal policy.

        possible values are "fixed", "minimum", "maximum", "preferred",
        "expanding", "minimum_expanding" and "ignored"

        Args:
            mode: policy to set
        """
        self.setHorizontalPolicy(SIZE_POLICIES[mode])

    def get_vertical_policy(self) -> str:
        """Return size policy.

        possible values are "fixed", "minimum", "maximum", "preferred",
        "expanding", "minimum_expanding" and "ignored"

        Returns:
            vertical size policy
        """
        return SIZE_POLICIES.inv[self.verticalPolicy()]

    def set_vertical_policy(self, mode: str) -> None:
        """Set the horizontal policy.

        possible values are "fixed", "minimum", "maximum", "preferred",
        "expanding", "minimum_expanding" and "ignored"

        Args:
            mode: policy to set
        """
        self.setVerticalPolicy(SIZE_POLICIES[mode])

    def get_control_type(self) -> str:
        """Return control type.

        possible values are "default", "buttonbox", "checkbox", "combobox", "frame",
        "groupbox", "label", "line", "lineedit", "pushbutton", "radiobutton", "slider",
        "spinbox", "tabwidget", "toolbutton"

        Returns:
            control type
        """
        return CONTROL_TYPES.inv[self.controlType()]

    def set_control_type(self, mode: str) -> None:
        """Set the control type.

        possible values are "default", "buttonbox", "checkbox", "combobox", "frame",
        "groupbox", "label", "line", "lineedit", "pushbutton", "radiobutton", "slider",
        "spinbox", "tabwidget", "toolbutton"

        Args:
            mode: control type to set
        """
        self.setControlType(CONTROL_TYPES[mode])
