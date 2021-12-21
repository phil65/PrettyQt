from __future__ import annotations

import os
from typing import Callable, Literal

from prettyqt import constants, core, gui, iconprovider
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, helpers, prettyprinter, types


PRIORITIES = bidict(
    low=QtWidgets.QAction.Priority.LowPriority,
    normal=QtWidgets.QAction.Priority.NormalPriority,
    high=QtWidgets.QAction.Priority.HighPriority,
)

PriorityStr = Literal["low", "normal", "high"]

ROLES = bidict(
    none=QtWidgets.QAction.MenuRole.NoRole,
    text_heuristic=QtWidgets.QAction.MenuRole.TextHeuristicRole,
    application_specific=QtWidgets.QAction.MenuRole.ApplicationSpecificRole,
    about_qt=QtWidgets.QAction.MenuRole.AboutQtRole,
    about=QtWidgets.QAction.MenuRole.AboutRole,
    preferences=QtWidgets.QAction.MenuRole.PreferencesRole,
    quit=QtWidgets.QAction.MenuRole.QuitRole,
)

RoleStr = Literal[
    "none",
    "text_heuristic",
    "application_specific",
    "about_qt",
    "about",
    "preferences",
    "quit",
]

QtWidgets.QAction.__bases__ = (core.Object,)


class Action(prettyprinter.PrettyPrinter, QtWidgets.QAction):
    def __init__(
        self,
        parent: QtCore.QObject | None = None,
        text: str = "",
        icon: types.IconType = None,
        shortcut: str | None = None,
        tooltip: str = "",
        checkable: bool = False,
        checked: bool = False,
        statustip: str = "",
        enabled: bool = True,
        callback: Callable | None = None,
    ):
        super().__init__(parent)
        self._menu = None
        self.set_text(text)
        self.set_icon(icon)
        self.set_shortcut(shortcut)
        self.set_tooltip(tooltip)
        self.set_checkable(checkable)
        self.set_checked(checked)
        self.set_statustip(statustip)
        self.set_enabled(enabled)
        if callback is not None:
            self.triggered.connect(callback)

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}({helpers.format_kwargs(self.serialize_fields())})"

    def serialize_fields(self):
        dct = dict(
            auto_repeat=self.autoRepeat(),
            text=self.text(),
            enabled=self.isEnabled(),
            visible=self.isVisible(),
            font=self.get_font(),
            shortcut=self.get_shortcut(),
            tool_tip=self.toolTip(),
            checkable=self.isCheckable(),
            checked=self.isChecked(),
            icon=self.get_icon(),
            icon_text=self.iconText(),
            priority=self.get_priority(),
            icon_visible_in_menu=self.isIconVisibleInMenu(),
            shortcut_visible_in_context_menu=self.isShortcutVisibleInContextMenu(),
            menu_role=self.get_menu_role(),
            shortcut_context=self.get_shortcut_context(),
            status_tip=self.statusTip(),
            whats_this=self.whatsThis(),
        )
        if core.VersionNumber.get_qt_version() < (6, 0, 0):
            dct["menu"] = self.menu()
        return dct

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_text(state.get("text", ""))
        self.set_enabled(state.get("enabled", True))
        self.set_shortcut(state["shortcut"])
        self.set_tooltip(state.get("tool_tip", ""))
        self.set_statustip(state.get("status_tip", ""))
        self.set_checked(state.get("checked", False))
        self.set_priority(state["priority"])
        self.set_shortcut_context(state["shortcut_context"])
        self.set_checkable(state["checkable"])
        self.setAutoRepeat(state["auto_repeat"])
        self.setVisible(state["visible"])
        self.setFont(state["font"])
        # self.setIcon(state["icon"])
        self.setIconText(state["icon_text"])
        self.setIconVisibleInMenu(state["icon_visible_in_menu"])
        self.setShortcutVisibleInContextMenu(state["shortcut_visible_in_context_menu"])
        self.set_menu_role(state["menu_role"])
        self.setWhatsThis(state["whats_this"])
        # if core.VersionNumber.get_qt_version() < (6, 0, 0):
        #     self.setMenu(state["menu"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_text(self, text: str):
        self.setText(text)

    def set_enabled(self, enabled: bool = True):
        self.setEnabled(enabled)

    def set_disabled(self):
        self.setEnabled(False)

    def set_tooltip(
        self,
        tooltip: str | types.PathType,
        size: types.SizeType | None = None,
    ):
        if isinstance(tooltip, os.PathLike):
            path = os.fspath(tooltip)
            if size is None:
                tooltip = f"<img src={path!r}>"
            else:
                if isinstance(size, QtCore.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        self.setToolTip(tooltip)

    def set_statustip(self, text: str):
        self.setStatusTip(text)

    def set_checked(self, value: bool):
        self.setChecked(value)

    def set_checkable(self, value: bool):
        self.setCheckable(value)

    def set_icon(self, icon: types.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        if icon.isNull():
            return None
        return gui.Icon(icon)

    def set_shortcut(self, shortcut: None | QtGui.QKeySequence | str):
        if shortcut is None:
            shortcut = ""
        if isinstance(shortcut, str):
            shortcut = gui.KeySequence(
                shortcut, gui.KeySequence.SequenceFormat.PortableText
            )
        self.setShortcut(shortcut)

    def get_shortcut(self) -> gui.KeySequence | None:
        shortcut = self.shortcut()
        if not shortcut:
            return None
        return gui.KeySequence(
            shortcut.toString(), gui.KeySequence.SequenceFormat.PortableText
        )

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def set_menu(self, menu):
        try:
            self.setMenu(menu)
        except AttributeError:
            self.triggered.connect(menu.exec_)
            self._menu = menu

    def menu(self):
        return self._menu

    def set_priority(self, priority: PriorityStr):
        """Set priority of the action.

        Args:
            priority: priority for the action

        Raises:
            InvalidParamError: priority does not exist
        """
        if priority not in PRIORITIES:
            raise InvalidParamError(priority, PRIORITIES)
        self.setPriority(PRIORITIES[priority])

    def get_priority(self) -> PriorityStr:
        """Return current priority.

        Returns:
            priority
        """
        return PRIORITIES.inverse[self.priority()]

    def set_shortcut_context(self, context: constants.ContextStr):
        """Set shortcut context.

        Args:
            context: shortcut context

        Raises:
            InvalidParamError: shortcut context does not exist
        """
        if context not in constants.CONTEXT:
            raise InvalidParamError(context, constants.CONTEXT)
        self.setShortcutContext(constants.CONTEXT[context])

    def get_shortcut_context(self) -> constants.ContextStr:
        """Return shortcut context.

        Returns:
            shortcut context
        """
        return constants.CONTEXT.inverse[self.shortcutContext()]

    def set_menu_role(self, role: RoleStr):
        """Set menu role.

        Args:
            role: menu role

        Raises:
            InvalidParamError: menu role does not exist
        """
        if role not in ROLES:
            raise InvalidParamError(role, ROLES)
        self.setMenuRole(ROLES[role])

    def get_menu_role(self) -> RoleStr:
        """Return menu role.

        Returns:
            menu role
        """
        return ROLES.inverse[self.menuRole()]

    def show_shortcut_in_contextmenu(self, state: bool = True):
        self.setShortcutVisibleInContextMenu(state)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    action = Action(text="This is a test")
