from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, Literal, Optional, Union

from deprecated import deprecated
import qstylizer.parser
import qstylizer.style
from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import InvalidParamError, colors, helpers, prettyprinter


QtWidgets.QWidget.__bases__ = (core.Object, QtGui.QPaintDevice)


LayoutStr = Literal["horizontal", "vertical", "grid", "form", "stacked", "flow"]


class Widget(prettyprinter.PrettyPrinter, QtWidgets.QWidget):
    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        params = helpers.format_kwargs(self.serialize_fields())
        return f"{cls_name}({params})"

    def __setstate__(self, state: Dict[str, Any]) -> None:
        if self.layout() is None:
            self.set_layout(state["layout"])
        self.setSizePolicy(state["size_policy"])
        self.setAccessibleName(state["accessible_name"])
        self.setToolTip(state.get("tool_tip", ""))
        self.setStatusTip(state.get("status_tip", ""))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self) -> Dict[str, Any]:
        icon = gui.Icon(self.windowIcon())
        return dict(
            layout=self.layout() if isinstance(self.layout(), widgets.Layout) else None,
            size_policy=self.get_size_policy(),
            actions=self.actions(),
            accessible_name=self.accessibleName(),
            tool_tip=self.toolTip(),
            tooltip_duration=self.toolTipDuration(),
            window_title=self.windowTitle(),
            enabled=self.isEnabled(),
            visible=self.isVisible(),
            stylesheet=self.styleSheet(),
            icon=icon if not icon.isNull() else None,
            modality=self.get_modality(),
            whats_this=self.whatsThis(),
            contextmenu_policy=self.get_contextmenu_policy(),
            focus_policy=self.get_focus_policy(),
            status_tip=self.statusTip(),
        )

    def resize(self, *size) -> None:
        if isinstance(size[0], tuple):
            super().resize(*size[0])
        else:
            super().resize(*size)

    def set_icon(self, icon: gui.icon.IconType) -> None:
        """Set the window icon.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon, color=colors.WINDOW_ICON_COLOR)
        self.setWindowIcon(icon)

    def set_min_size(self, *size) -> None:
        self.setMinimumSize(*size)

    def set_max_size(self, *size) -> None:
        self.setMaximumSize(*size)

    def set_min_width(self, width: Optional[int]) -> None:
        if width is None:
            width = 0
        self.setMinimumWidth(width)

    def set_max_width(self, width: Optional[int]) -> None:
        if width is None:
            width = 16777215  # QtWidgets.QWIDGETSIZE_MAX
        self.setMaximumWidth(width)

    def set_min_height(self, height: Optional[int]) -> None:
        if height is None:
            height = 0
        self.setMinimumHeight(height)

    def set_max_height(self, height: Optional[int]) -> None:
        if height is None:
            height = 16777215  # QtWidgets.QWIDGETSIZE_MAX
        self.setMaximumHeight(height)

    @property
    def title(self) -> str:
        return self.windowTitle()

    @title.setter
    def title(self, name: str):
        self.setWindowTitle(name)

    @property
    def enabled(self) -> bool:
        return self.isEnabled()

    @enabled.setter
    def enabled(self, state: bool):
        self.setEnabled(state)

    def set_enabled(self, enabled: bool = True) -> None:
        self.setEnabled(enabled)

    def set_disabled(self) -> None:
        self.setEnabled(False)

    def set_title(self, title: str) -> None:
        self.setWindowTitle(title)

    def get_title(self) -> str:
        return self.windowTitle()

    def set_tooltip(self, text: str) -> None:
        self.setToolTip(text)

    def set_font(
        self,
        font_name: Optional[str] = None,
        font_size: int = -1,
        weight: int = -1,
        italic: bool = False,
    ) -> gui.Font:
        if font_name is None:
            font_name = self.font().family()
        font = gui.Font(font_name, font_size, weight, italic)
        self.setFont(font)
        return font

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def set_window_flags(self, *flags: constants.WindowFlagStr, append: bool = False):
        for flag in flags:
            if flag not in constants.WINDOW_FLAGS:
                raise InvalidParamError(flag, constants.WINDOW_FLAGS)
        result = helpers.merge_flags(flags, constants.WINDOW_FLAGS)
        if append:
            result = result | self.windowFlags()
        self.setWindowFlags(result)

    def set_flags(
        self,
        minimize: Optional[bool] = None,
        maximize: Optional[bool] = None,
        close: Optional[bool] = None,
        stay_on_top: Optional[bool] = None,
        frameless: Optional[bool] = None,
        window: Optional[bool] = None,
    ) -> None:
        if minimize is not None:
            self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, minimize)
        if maximize is not None:
            self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, maximize)
        if close is not None:
            self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, close)
        if stay_on_top is not None:
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, stay_on_top)
        if frameless is not None:
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint, frameless)
        if window is not None:
            self.setWindowFlag(QtCore.Qt.Window, window)

    def set_attribute(
        self, attribute: constants.WindowAttributeStr, state: bool = True
    ) -> None:
        if attribute not in constants.WINDOW_ATTRIBUTES:
            raise InvalidParamError(attribute, constants.WINDOW_ATTRIBUTES)
        self.setAttribute(constants.WINDOW_ATTRIBUTES[attribute], state)

    def set_attributes(self, **kwargs: Dict[constants.WindowAttributeStr, bool]) -> None:
        for attribute, state in kwargs.items():
            if attribute not in constants.WINDOW_ATTRIBUTES:
                raise InvalidParamError(attribute, constants.WINDOW_ATTRIBUTES)
            self.setAttribute(constants.WINDOW_ATTRIBUTES[attribute], state)

    def set_modality(self, modality: constants.ModalityStr) -> None:
        """Set modality for the dialog.

        Args:
            modality: modality for the main window

        Raises:
            InvalidParamError: modality type does not exist
        """
        if modality not in constants.MODALITY:
            raise InvalidParamError(modality, constants.MODALITY)
        self.setWindowModality(constants.MODALITY[modality])

    def get_modality(self) -> constants.ModalityStr:
        """Get the current modality modes as a string.

        Returns:
            modality mode
        """
        return constants.MODALITY.inverse[self.windowModality()]

    def set_size_policy(
        self,
        horizontal: Optional[widgets.sizepolicy.SizePolicyStr] = None,
        vertical: Optional[widgets.sizepolicy.SizePolicyStr] = None,
    ) -> None:
        """Set the sizes policy.

        Args:
            horizontal: horizontal size policy
            vertical: vertical size policy
        """
        sp = self.get_size_policy()
        if horizontal is not None:
            sp.set_horizontal_policy(horizontal)
        if vertical is not None:
            sp.set_vertical_policy(vertical)
        self.setSizePolicy(sp)

    def get_size_policy(self) -> widgets.SizePolicy:
        qpol = self.sizePolicy()
        if isinstance(qpol, widgets.SizePolicy):
            return qpol
        pol = widgets.SizePolicy(
            qpol.horizontalPolicy(), qpol.verticalPolicy(), qpol.controlType()
        )
        pol.setHeightForWidth(qpol.hasHeightForWidth())
        pol.setWidthForHeight(qpol.hasWidthForHeight())
        pol.setHorizontalStretch(qpol.horizontalStretch())
        pol.setVerticalStretch(qpol.verticalStretch())
        return pol

    def get_palette(self) -> gui.Palette:
        return gui.Palette(self.palette())

    def set_background_color(self, color: colors.ColorType) -> None:
        col_str = "" if color is None else colors.get_color(color).name()
        with self.edit_stylesheet() as ss:
            ss.backgroundColor.setValue(col_str)

    @contextmanager
    def updates_off(self) -> Iterator[None]:
        self.setUpdatesEnabled(False)
        yield None
        self.setUpdatesEnabled(True)

    @contextmanager
    def edit_stylesheet(self) -> Iterator[qstylizer.style.StyleSheet]:
        ss = qstylizer.parser.parse(self.styleSheet())
        yield ss
        self.setStyleSheet(ss.toString())

    @contextmanager
    def edit_palette(self) -> Iterator[gui.Palette]:
        palette = gui.Palette(self.palette())
        yield palette
        self.setPalette(palette)

    @contextmanager
    def edit_font(self) -> Iterator[gui.Font]:
        font = gui.Font(self.font())
        yield font
        self.setFont(font)

    @deprecated(reason="This context manager is deprecated, use edit_font instead.")
    @contextmanager
    def current_font(self) -> Iterator[gui.Font]:
        with self.edit_font() as font:
            yield font

    def set_contextmenu_policy(self, policy: constants.ContextPolicyStr) -> None:
        """Set contextmenu policy for given item view.

        Args:
            policy: contextmenu policy to use

        Raises:
            InvalidParamError: policy does not exist
        """
        if policy not in constants.CONTEXT_POLICY:
            raise InvalidParamError(policy, constants.CONTEXT_POLICY)
        self.setContextMenuPolicy(constants.CONTEXT_POLICY[policy])

    def get_contextmenu_policy(self) -> constants.ContextPolicyStr:
        """Return current contextmenu policy.

        Returns:
            contextmenu policy
        """
        return constants.CONTEXT_POLICY.inverse[self.contextMenuPolicy()]

    def set_window_state(self, policy: constants.WindowStateStr) -> None:
        """Set window state for given item view.

        Args:
            policy: window state to use

        Raises:
            InvalidParamError: policy does not exist
        """
        if policy not in constants.WINDOW_STATES:
            raise InvalidParamError(policy, constants.WINDOW_STATES)
        self.setWindowState(constants.WINDOW_STATES[policy])

    def get_window_state(self) -> constants.WindowStateStr:
        """Return current window state.

        Returns:
            window state
        """
        return constants.WINDOW_STATES.inverse[self.windowState()]

    def set_custom_menu(self, method: Callable) -> None:
        self.set_contextmenu_policy("custom")
        self.customContextMenuRequested.connect(method)

    def set_layout(
        self,
        layout: Union[LayoutStr, QtWidgets.QLayout, None],
        margin: Optional[int] = None,
        spacing: Optional[int] = None,
    ) -> None:
        if layout is None:
            return None
        if layout in ["horizontal", "vertical"]:
            self.box = widgets.BoxLayout(layout)
        elif layout == "grid":
            self.box = widgets.GridLayout()
        elif layout == "form":
            self.box = widgets.FormLayout()
        elif layout == "stacked":
            self.box = widgets.StackedLayout()
        elif layout == "flow":
            from prettyqt import custom_widgets

            self.box = custom_widgets.FlowLayout()
        elif isinstance(layout, QtWidgets.QLayout):
            self.box = layout
        else:
            raise ValueError("Invalid Layout")
        self.setLayout(self.box)
        if margin is not None:
            self.box.set_margin(margin)
        if spacing is not None:
            self.box.setSpacing(spacing)

    def center(self) -> None:
        qr = self.frameGeometry()
        cp = gui.GuiApplication.screens()[0].geometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_cursor(self, cursor: constants.CursorShapeStr) -> None:
        if cursor not in constants.CURSOR_SHAPE:
            raise InvalidParamError(cursor, constants.CURSOR_SHAPE)
        self.setCursor(constants.CURSOR_SHAPE[cursor])

    def set_focus_policy(self, policy: constants.FocusPolicyStr) -> None:
        """Set the way the widget accepts keyboard focus.

        Args:
            policy (str): Focus policy

        Raises:
            InvalidParamError: Description
        """
        if policy not in constants.FOCUS_POLICY:
            raise InvalidParamError(policy, constants.FOCUS_POLICY)
        self.setFocusPolicy(constants.FOCUS_POLICY[policy])

    def get_focus_policy(self) -> constants.FocusPolicyStr:
        """Return waay the widget accepts keyboard focus.

        Returns:
            str: Focus policy
        """
        return constants.FOCUS_POLICY.inverse[self.focusPolicy()]

    def set_font_size(self, size: int) -> None:
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    @deprecated(reason="This method is deprecated, use get_font_metrics instead.")
    def font_metrics(self) -> gui.FontMetrics:
        return self.get_font_metrics()

    def get_font_metrics(self) -> gui.FontMetrics:
        return gui.FontMetrics(self.fontMetrics())

    def get_font_info(self) -> gui.FontInfo:
        return gui.FontInfo(self.fontInfo())

    def set_margin(self, margin: int) -> None:
        self.setContentsMargins(margin, margin, margin, margin)

    def raise_dock(self) -> bool:
        w = self.find_parent(QtWidgets.QDockWidget)
        if w is None:
            return False
        w.setVisible(True)
        w.raise_()
        return True

    def set_mask(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        typ: gui.region.RegionTypeStr = "rectangle",
    ):
        self.setMask(gui.Region(x, y, width, height, gui.region.REGION_TYPE[typ]))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.main_loop()
