from __future__ import annotations

from collections.abc import Callable
import html
import os
from typing import Literal

from prettyqt import constants, core, gui, iconprovider
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import bidict, datatypes, get_repr


ACTION_EVENT = bidict(
    trigger=QtGui.QAction.ActionEvent.Trigger,
    hover=QtGui.QAction.ActionEvent.Hover,
)

ActionEventStr = Literal["trigger", "hover"]


PRIORITIES = bidict(
    low=QtGui.QAction.Priority.LowPriority,
    normal=QtGui.QAction.Priority.NormalPriority,
    high=QtGui.QAction.Priority.HighPriority,
)

PriorityStr = Literal["low", "normal", "high"]

ROLES = bidict(
    none=QtGui.QAction.MenuRole.NoRole,
    text_heuristic=QtGui.QAction.MenuRole.TextHeuristicRole,
    application_specific=QtGui.QAction.MenuRole.ApplicationSpecificRole,
    about_qt=QtGui.QAction.MenuRole.AboutQtRole,
    about=QtGui.QAction.MenuRole.AboutRole,
    preferences=QtGui.QAction.MenuRole.PreferencesRole,
    quit=QtGui.QAction.MenuRole.QuitRole,
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


class ActionMixin(core.ObjectMixin):
    def __init__(
        self,
        *args,
        text: str | None = None,
        icon: datatypes.IconType = None,
        callback: Callable | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if callback is not None:
            self.triggered.connect(callback)
        self._usage_count = 0
        if text:
            self.setText(text)
        if icon:
            self.set_icon(icon)
        self.triggered.connect(self._increase_usage_counter)

    def __repr__(self) -> str:
        return get_repr(self, self.text())

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "priority": PRIORITIES,
            "shortcutContext": constants.SHORTCUT_CONTEXT,
            "menuRole": ROLES,
        }
        return maps

    def _increase_usage_counter(self):
        self._usage_count += 1

    def get_usage_count(self) -> int:
        return self._usage_count

    def get_type(self) -> Literal["menu", "separator", "widget", "regular"]:
        if self.menu() is not None:
            return "menu"
        elif self.isSeparator():
            return "separator"
        elif hasattr(self, "defaultWidget"):
            return "widget"
        else:
            return "regular"

    def set_disabled(self):
        self.setEnabled(False)

    def set_enabled(self, enabled: bool = True):
        self.setEnabled(enabled)

    def set_tooltip(
        self,
        tooltip: str | datatypes.PathType,
        size: datatypes.SizeType | None = None,
        rich_text: bool = False,
    ):
        if isinstance(tooltip, os.PathLike):
            path = os.fspath(tooltip)
            if size is None:
                tooltip = f"<img src={path!r}>"
            else:
                if isinstance(size, QtCore.QSize):
                    size = (size.width(), size.height())
                tooltip = f'<img src={path!r} width="{size[0]}" height="{size[1]}">'
        tooltip = tooltip.replace("\n", "<br/>")
        if rich_text:
            tooltip = f"<html>{html.escape(tooltip)}</html>"
        super().setToolTip(tooltip)

    setToolTip = set_tooltip

    def set_icon(self, icon: datatypes.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        super().setIcon(icon)

    setIcon = set_icon

    def set_shortcut(self, shortcut: None | QtGui.QKeySequence | str):
        if shortcut is None:
            shortcut = ""
        if isinstance(shortcut, str):
            shortcut = gui.KeySequence(
                shortcut, gui.KeySequence.SequenceFormat.PortableText
            )
        super().setShortcut(shortcut)

    setShortcut = set_shortcut

    def setText(self, text: str | None):
        super().setText(text or "")

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

    def get_shortcut(self) -> gui.KeySequence | None:
        shortcut = self.shortcut()
        return (
            gui.KeySequence(
                shortcut.toString(), gui.KeySequence.SequenceFormat.PortableText
            )
            if shortcut
            else None
        )

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def set_menu(self, menu):
        self.setMenu(menu)

    def set_priority(self, priority: PriorityStr | QtGui.QAction.Priority):
        """Set priority of the action.

        Args:
            priority: priority for the action

        Raises:
            InvalidParamError: priority does not exist
        """
        if isinstance(priority, str):
            priority = PRIORITIES[priority]
        super().setPriority(priority)

    setPriority = set_priority

    def get_priority(self) -> PriorityStr:
        """Return current priority.

        Returns:
            priority
        """
        return PRIORITIES.inverse[self.priority()]

    def set_shortcut_context(
        self, context: constants.ShortcutContextStr | QtCore.Qt.ShortcutContext
    ):
        """Set shortcut context.

        Args:
            context: shortcut context

        Raises:
            InvalidParamError: shortcut context does not exist
        """
        if isinstance(context, str):
            context = constants.SHORTCUT_CONTEXT[context]
        super().setShortcutContext(context)

    setShortcutContext = set_shortcut_context

    def get_shortcut_context(self) -> constants.ShortcutContextStr:
        """Return shortcut context.

        Returns:
            shortcut context
        """
        return constants.SHORTCUT_CONTEXT.inverse[super().shortcutContext()]

    def set_menu_role(self, role: RoleStr):
        """Set menu role.

        Args:
            role: menu role

        Raises:
            InvalidParamError: menu role does not exist
        """
        if isinstance(role, str):
            role = ROLES[role]
        super().setMenuRole(role)

    setMenuRole = set_menu_role

    def get_menu_role(self) -> RoleStr:
        """Return menu role.

        Returns:
            menu role
        """
        return ROLES.inverse[super().menuRole()]

    def show_shortcut_in_contextmenu(self, state: bool = True):
        self.setShortcutVisibleInContextMenu(state)

    usage_count = core.Property(int, get_usage_count)


class Action(ActionMixin, QtGui.QAction):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    action = Action(text="This is a test", shortcut=None)
