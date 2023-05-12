from __future__ import annotations

from collections.abc import Callable
import os
from typing import Literal

from prettyqt import constants, core, gui, iconprovider
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import InvalidParamError, bidict, datatypes, get_repr, prettyprinter


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
        self._menu = None
        if callback is not None:
            self.triggered.connect(callback)
        self._usage_count = 0
        if text:
            self.setText(text)
        if icon:
            self.set_icon(icon)
        self.triggered.connect(self._increase_usage_counter)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "priority": PRIORITIES,
        }
        return maps

    def _increase_usage_counter(self):
        self._usage_count += 1

    def get_usage_count(self) -> int:
        return self._usage_count

    def __repr__(self) -> str:
        return get_repr(self, self.text())

    def get_type(self) -> Literal["menu", "separator", "widget", "regular"]:
        if self.menu() is not None:
            return "menu"
        elif self.isSeparator():
            return "separator"
        elif hasattr(self, "defaultWidget"):
            return "widget"
        else:
            return "regular"

    def set_text(self, text: str):
        self.setText(text)

    def set_enabled(self, enabled: bool = True):
        self.setEnabled(enabled)

    def set_disabled(self):
        self.setEnabled(False)

    def set_tooltip(
        self,
        tooltip: str | datatypes.PathType,
        size: datatypes.SizeType | None = None,
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
        self.setToolTip(tooltip)

    def set_statustip(self, text: str):
        self.setStatusTip(text)

    def set_checked(self, value: bool):
        self.setChecked(value)

    def set_checkable(self, value: bool):
        self.setCheckable(value)

    def set_icon(self, icon: datatypes.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def get_icon(self) -> gui.Icon | None:
        icon = self.icon()
        return None if icon.isNull() else gui.Icon(icon)

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
        try:
            self.setMenu(menu)
        except AttributeError:
            self.triggered.connect(menu.exec)
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

    def set_shortcut_context(self, context: constants.ShortcutContextStr):
        """Set shortcut context.

        Args:
            context: shortcut context

        Raises:
            InvalidParamError: shortcut context does not exist
        """
        if context not in constants.SHORTCUT_CONTEXT:
            raise InvalidParamError(context, constants.SHORTCUT_CONTEXT)
        self.setShortcutContext(constants.SHORTCUT_CONTEXT[context])

    def get_shortcut_context(self) -> constants.ShortcutContextStr:
        """Return shortcut context.

        Returns:
            shortcut context
        """
        return constants.SHORTCUT_CONTEXT.inverse[self.shortcutContext()]

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

    usage_count = core.Property(int, get_usage_count)


class Action(ActionMixin, prettyprinter.PrettyPrinter, QtGui.QAction):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    action = Action(text="This is a test")
