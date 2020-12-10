# -*- coding: utf-8 -*-

from typing import Callable, Optional, Dict, Any, Union, Tuple

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict, InvalidParamError, helpers


STYLE = bidict(
    icon=QtCore.Qt.ToolButtonIconOnly,
    text=QtCore.Qt.ToolButtonTextOnly,
    text_beside_icon=QtCore.Qt.ToolButtonTextBesideIcon,
    text_below_icon=QtCore.Qt.ToolButtonTextUnderIcon,
)

TOOLBAR_AREAS = bidict(
    left=QtCore.Qt.LeftToolBarArea,
    right=QtCore.Qt.RightToolBarArea,
    top=QtCore.Qt.TopToolBarArea,
    bottom=QtCore.Qt.BottomToolBarArea,
    all=QtCore.Qt.AllToolBarAreas,
    none=QtCore.Qt.NoToolBarArea,
)


QtWidgets.QToolBar.__bases__ = (widgets.Widget,)


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon_size(24)
        self.menu_buttons = list()

    def __setstate__(self, state: Dict[str, Any]) -> None:
        super().__init__()
        self.addActions(state["actions"])

    def add_menu_button(
        self, label: str, icon: gui.icon.IconType, menu: QtWidgets.QMenu
    ) -> widgets.ToolButton:
        btn = widgets.ToolButton.for_menu(menu)
        btn.setText(label)
        btn.setToolButtonStyle(self.toolButtonStyle())
        btn.set_icon(icon)
        self.menu_buttons.append(btn)
        self.addWidget(btn)
        return btn

    def add_separator(
        self, text: Optional[str] = None, before: QtWidgets.QAction = None
    ) -> QtWidgets.QAction:
        """Adds a separator showing an optional label.

        Args:
            text: Text to show on separator
            before: insert separator before specific action

        Returns:
            Separator action
        """
        if text is None:
            if before:
                return self.insertSeparator(before)
            else:
                return self.addSeparator()
        else:
            label = widgets.Label(text)
            label.setMinimumWidth(self.minimumWidth())
            with label.edit_stylesheet() as ss:
                ss.background.setValue("lightgrey")
            label.set_alignment(horizontal="center")
            if before:
                return self.insertWidget(before, label)
            else:
                return self.addWidget(label)

    def set_style(self, style: str):
        self.setToolButtonStyle(STYLE[style])
        for btn in self.menu_buttons:
            btn.set_style(style)

    def get_style(self) -> str:
        """Return current style.

        Possible values: "icon", "text", "text_below_icon", "text_beside_icon"

        Returns:
            style
        """
        return STYLE.inv[self.toolButtonStyle()]

    def add_action(
        self,
        label: str,
        icon: gui.icon.IconType = None,
        callback: Optional[Callable] = None,
        checkable: bool = False,
    ) -> QtWidgets.QAction:
        icon = gui.icon.get_icon(icon)
        action = self.addAction(icon, label)
        if callback is not None:
            action.triggered.connect(callback)
        if checkable:
            action.setCheckable(True)
        return action

    def add_spacer(self) -> QtWidgets.QAction:
        spacer = widgets.Widget()
        spacer.set_size_policy("expanding", "expanding")
        return self.addWidget(spacer)

    def set_icon_size(self, size: Union[int, Tuple[int, int], QtCore.QSize]):
        """Set size of the icons."""
        if isinstance(size, int):
            size = core.Size(size, size)
        elif isinstance(size, tuple):
            size = core.Size(*size)
        self.setIconSize(size)

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())

    def set_font_size(self, size: int):
        with self.edit_font() as font:
            font.set_size(size)

    def is_area_allowed(self, area: str) -> bool:
        """Check if toolbar is allowed at specified area.

        Valid values for area: "left", "right", "top", "bottom", "all"

        Args:
            area: area of the toolbar

        Raises:
            InvalidParamError: area does not exist
        """
        if area not in TOOLBAR_AREAS:
            raise InvalidParamError(area, TOOLBAR_AREAS)
        return self.isAreaAllowed(TOOLBAR_AREAS[area])

    def set_allowed_areas(self, *areas: str):
        for area in areas:
            if area not in TOOLBAR_AREAS:
                raise InvalidParamError(area, TOOLBAR_AREAS)
        flag = helpers.merge_flags(areas, TOOLBAR_AREAS)
        self.setAllowedAreas(flag)


if __name__ == "__main__":
    app = widgets.app()
    widget = ToolBar()
    widget.show()
    app.main_loop()
