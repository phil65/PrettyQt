from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, datatypes, get_repr


# from typing import Any


class ToolBarMixin(widgets.WidgetMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon_size(24)
        self._menu_buttons = []
        self._tooltip_labels = []
        self._tooltip_timer = core.Timer(timeout=self.hide_tooltips)

    # def __setstate__(self, state: dict[str, Any]) -> None:
    #     super().__setstate__(state)
    #     self.addActions(state["actions"])

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()

    # def serialize_fields(self):
    #     return dict(actions=self.actions(), allowed_areas=self.get_allowed_areas())

    def __repr__(self):
        return get_repr(self, self.windowTitle())

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "toolButtonStyle": constants.TOOLBUTTON_STYLE,
            "allowedAreas": constants.TOOLBAR_AREA,
        }
        return maps

    def add(self, item: QtGui.QAction | QtWidgets.QWidget):
        if isinstance(item, QtGui.QAction):
            self.addAction(item)
        else:
            self.addWidget(item)

    def add_menu_button(
        self, label: str, icon: datatypes.IconType, menu: QtWidgets.QMenu
    ) -> widgets.ToolButton:
        btn = widgets.ToolButton.for_menu(menu, icon=icon)
        btn.setText(label)
        btn.setToolButtonStyle(self.toolButtonStyle())
        self._menu_buttons.append(btn)
        self.addWidget(btn)
        return btn

    def add_separator(
        self, text: str | None = None, before: QtGui.QAction | None = None
    ) -> QtGui.QAction:
        """Adds a separator showing an optional label.

        Args:
            text: Text to show on separator
            before: insert separator before specific action

        Returns:
            Separator action
        """
        if text is None:
            return self.insertSeparator(before) if before else self.addSeparator()
        label = widgets.Label(text)
        label.setMinimumWidth(self.minimumWidth())
        with label.edit_stylesheet() as ss:
            ss.background.setValue("lightgrey")
        label.set_alignment(horizontal="center")
        return self.insertWidget(before, label) if before else self.addWidget(label)

    def set_style(self, style: constants.ToolButtonStyleStr):
        self.setToolButtonStyle(constants.TOOLBUTTON_STYLE[style])
        for btn in self._menu_buttons:
            btn.set_style(style)

    def get_style(self) -> constants.ToolButtonStyleStr:
        """Return current style.

        Returns:
            style
        """
        return constants.TOOLBUTTON_STYLE.inverse[self.toolButtonStyle()]

    def add_spacer(self) -> QtGui.QAction:
        spacer = widgets.Widget()
        spacer.set_size_policy("expanding", "expanding")
        return self.addWidget(spacer)

    def set_icon_size(self, size: int | datatypes.SizeType):
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
        flag = constants.TOOLBAR_AREA.merge_flags(areas)
        self.setAllowedAreas(flag)

    def get_allowed_areas(self) -> list[constants.ToolbarAreaStr]:
        return constants.TOOLBAR_AREA.get_list(self.allowedAreas())

    def get_widgets(self) -> list[QtWidgets.QAction]:
        return [self.widgetForAction(i) for i in self.actions()]

    def show_tooltips(self, value: bool = True, duration_ms: int = 2000):
        """Show all the tooltips."""
        if self._tooltip_labels:
            self._tooltip_timer.start(duration_ms)
            return
        for i in self.get_widgets():
            label = widgets.Label(
                i.toolTip(), self, QtCore.Qt.WindowType.ToolTip, alignment="center"
            )
            label.setStyleSheet("border: 1px solid gray;")
            label.hide()
            pos = i.mapToGlobal(core.Point(0, 0))
            label.move(pos)
            label.show()
            self._tooltip_labels.append(label)
        self._tooltip_timer.start(duration_ms)

    def hide_tooltips(self):
        """Hide all the tooltips."""
        for label in self._tooltip_labels:
            label.hide()
            label.deleteLater()
        self._tooltip_labels = []


class ToolBar(ToolBarMixin, QtWidgets.QToolBar):
    pass


if __name__ == "__main__":
    app = widgets.app()
    toolbar = ToolBar("test")
    toolbar.add_action(text="test", tool_tip="tesf dsfsdfdsfdsfsdfsdffst")
    toolbar.add_action(text="test2", tool_tip="test2")
    radio = widgets.RadioButton("abc")
    action = toolbar.addWidget(radio)

    toolbar.show()
    toolbar.show_tooltips()
    app.main_loop()
