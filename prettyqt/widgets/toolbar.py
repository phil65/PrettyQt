from __future__ import annotations

from typing import Any, Callable

from prettyqt import constants, core, iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, helpers, types


QtWidgets.QToolBar.__bases__ = (widgets.Widget,)


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon_size(24)
        self.menu_buttons = list()

    def __setstate__(self, state: dict[str, Any]) -> None:
        super().__setstate__(state)
        self.addActions(state["actions"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self):
        return dict(actions=self.actions(), allowed_areas=self.get_allowed_areas())

    def __repr__(self):
        return f"{type(self).__name__}({self.windowTitle()!r})"

    def add(self, item: QtWidgets.QAction | QtWidgets.QWidget):
        if isinstance(item, QtWidgets.QAction):
            self.addAction(item)
        else:
            self.addWidget(item)

    def add_menu_button(
        self, label: str, icon: types.IconType, menu: QtWidgets.QMenu
    ) -> widgets.ToolButton:
        btn = widgets.ToolButton.for_menu(menu)
        btn.setText(label)
        btn.setToolButtonStyle(self.toolButtonStyle())
        btn.set_icon(icon)
        self.menu_buttons.append(btn)
        self.addWidget(btn)
        return btn

    def add_separator(
        self, text: str | None = None, before: QtWidgets.QAction = None
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

    def set_style(self, style: constants.ToolButtonStyleStr):
        self.setToolButtonStyle(constants.TOOLBUTTON_STYLE[style])
        for btn in self.menu_buttons:
            btn.set_style(style)

    def get_style(self) -> constants.ToolButtonStyleStr:
        """Return current style.

        Returns:
            style
        """
        return constants.TOOLBUTTON_STYLE.inverse[self.toolButtonStyle()]

    def add_action(
        self,
        label: str,
        icon: types.IconType = None,
        callback: Callable | None = None,
        checkable: bool = False,
    ) -> QtWidgets.QAction:
        icon = iconprovider.get_icon(icon)
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

    def set_icon_size(self, size: int | types.SizeType):
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

    def is_area_allowed(self, area: constants.ToolbarAreaStr) -> bool:
        """Check if toolbar is allowed at specified area.

        Args:
            area: area of the toolbar

        Raises:
            InvalidParamError: area does not exist
        """
        if area not in constants.TOOLBAR_AREA:
            raise InvalidParamError(area, constants.TOOLBAR_AREA)
        return self.isAreaAllowed(constants.TOOLBAR_AREA[area])

    def set_allowed_areas(self, *areas: constants.ToolbarAreaStr):
        for area in areas:
            if area not in constants.TOOLBAR_AREA:
                raise InvalidParamError(area, constants.TOOLBAR_AREA)
        flag = helpers.merge_flags(areas, constants.TOOLBAR_AREA)
        self.setAllowedAreas(flag)

    def get_allowed_areas(self) -> list[constants.ToolbarAreaStr]:
        return [
            k
            for k, v in constants.TOOLBAR_AREA.items()
            if v & self.allowedAreas()  # type: ignore
        ]


if __name__ == "__main__":
    app = widgets.app()
    widget = ToolBar("test")
    widget.show()
    app.main_loop()
