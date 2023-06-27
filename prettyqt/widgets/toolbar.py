from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import datatypes, get_repr, listdelegators


# from typing import Any


class ToolBarMixin(widgets.WidgetMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon_size(24)
        self._menu_buttons = []
        self._tooltip_labels = []
        self._tooltip_timer = core.Timer(timeout=self.hide_tooltips)

    def __getitem__(
        self, row: int | slice
    ) -> QtWidgets.QWidget | listdelegators.BaseListDelegator[QtWidgets.QWidget]:
        match row:
            case int():
                action = self.actions()[row]
                if action is None:
                    raise KeyError(row)
                return self.widgetForAction(action)
            case slice():
                actions = self.actions()
                count = len(actions) if row.stop is None else row.stop
                values = list(range(count)[row])
                actions = [actions[i] for i in values]
                ls = [self.widgetForAction(i) for i in actions]
                return listdelegators.BaseListDelegator(ls)
            case _:
                raise TypeError(row)

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

    def set_style(self, style: constants.ToolButtonStyleStr | constants.ToolButtonStyle):
        self.setToolButtonStyle(constants.TOOLBUTTON_STYLE.get_enum_value(style))
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

    def set_icon_size(self, size: datatypes.SizeType):
        """Set size of the icons."""
        self.setIconSize(datatypes.to_size(size))

    def get_icon_size(self) -> core.Size:
        return core.Size(self.iconSize())

    def set_font_size(self, size: int):
        with self.edit_font() as font:
            font.set_size(size)

    def is_area_allowed(
        self, area: constants.ToolbarAreaStr | constants.ToolBarArea
    ) -> bool:
        """Check if toolbar is allowed at specified area.

        Args:
            area: area of the toolbar
        """
        return self.isAreaAllowed(constants.TOOLBAR_AREA.get_enum_value(area))

    def set_allowed_areas(self, *areas: constants.ToolbarAreaStr):
        flag = constants.TOOLBAR_AREA.merge_flags(areas)
        self.setAllowedAreas(flag)

    def get_allowed_areas(self) -> list[constants.ToolbarAreaStr]:
        return constants.TOOLBAR_AREA.get_list(self.allowedAreas())

    def get_widgets(self) -> listdelegators.BaseListDelegator[QtWidgets.QWidget]:
        widgets = [self.widgetForAction(i) for i in self.actions()]
        return listdelegators.BaseListDelegator(widgets)

    def show_tooltips(
        self,
        value: bool = True,
        duration_ms: int = 2000,
        content: Literal["tool_tip", "shortcut", "status_tip"] = "tool_tip",
    ):
        """Show all the tooltips."""
        if self._tooltip_labels:
            self._tooltip_timer.start(duration_ms)
            return
        for action, i in zip(self.actions(), self.get_widgets()):
            match content:
                case "tool_tip":
                    val = i.toolTip()
                case "shortcut":
                    val = action.shortcut().toString()
                case "status_tip":
                    val = i.statusTip()
                case _:
                    raise ValueError(content)
            if not val:
                continue
            label = widgets.Label(
                val, self, QtCore.Qt.WindowType.ToolTip, alignment="center"
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
    toolbar[0]
    toolbar.add_action(text="test", tool_tip="tesf dsfsdfdsfdsfsdfsdffst")
    toolbar.add_action(text="test2", tool_tip="test2")
    toolbar.add_action(text="test2", tool_tip="test2", shortcut="Ctrl+A")
    radio = widgets.RadioButton("abc")
    action = toolbar.addWidget(radio)
    toolbar.show()
    toolbar.show_tooltips(content="shortcut")
    app.exec()
