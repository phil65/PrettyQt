from __future__ import annotations

from collections.abc import Callable
import html
import os

from typing import Literal

from prettyqt import constants, core, gui, iconprovider
from prettyqt.utils import bidict, datatypes, get_repr


ActionEventStr = Literal["trigger", "hover"]

ACTION_EVENT: bidict[ActionEventStr, gui.QAction.ActionEvent] = bidict(
    trigger=gui.QAction.ActionEvent.Trigger,
    hover=gui.QAction.ActionEvent.Hover,
)

PriorityStr = Literal["low", "normal", "high"]

PRIORITIES: bidict[PriorityStr, gui.QAction.Priority] = bidict(
    low=gui.QAction.Priority.LowPriority,
    normal=gui.QAction.Priority.NormalPriority,
    high=gui.QAction.Priority.HighPriority,
)

MenuRoleStr = Literal[
    "none",
    "text_heuristic",
    "application_specific",
    "about_qt",
    "about",
    "preferences",
    "quit",
]

MENU_ROLE: bidict[MenuRoleStr, gui.QAction.MenuRole] = bidict(
    none=gui.QAction.MenuRole.NoRole,
    text_heuristic=gui.QAction.MenuRole.TextHeuristicRole,
    application_specific=gui.QAction.MenuRole.ApplicationSpecificRole,
    about_qt=gui.QAction.MenuRole.AboutQtRole,
    about=gui.QAction.MenuRole.AboutRole,
    preferences=gui.QAction.MenuRole.PreferencesRole,
    quit=gui.QAction.MenuRole.QuitRole,
)


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
            "menuRole": MENU_ROLE,
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
                if isinstance(size, core.QSize):
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

    def set_shortcut(self, shortcut: None | gui.QKeySequence | str):
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

    def set_priority(self, priority: PriorityStr | gui.QAction.Priority):
        """Set priority of the action.

        Args:
            priority: priority for the action
        """
        super().setPriority(PRIORITIES.get_enum_value(priority))

    setPriority = set_priority

    def get_priority(self) -> PriorityStr:
        """Return current priority.

        Returns:
            priority
        """
        return PRIORITIES.inverse[self.priority()]

    def set_shortcut_context(
        self, context: constants.ShortcutContextStr | constants.ShortcutContext
    ):
        """Set shortcut context.

        Args:
            context: shortcut context
        """
        super().setShortcutContext(constants.SHORTCUT_CONTEXT.get_enum_value(context))

    setShortcutContext = set_shortcut_context

    def get_shortcut_context(self) -> constants.ShortcutContextStr:
        """Return shortcut context.

        Returns:
            shortcut context
        """
        return constants.SHORTCUT_CONTEXT.inverse[super().shortcutContext()]

    def set_menu_role(self, role: MenuRoleStr | gui.QAction.MenuRole):
        """Set menu role.

        Args:
            role: menu role
        """
        super().setMenuRole(MENU_ROLE.get_enum_value(role))

    setMenuRole = set_menu_role

    def get_menu_role(self) -> MenuRoleStr:
        """Return menu role.

        Returns:
            menu role
        """
        return MENU_ROLE.inverse[super().menuRole()]

    def show_shortcut_in_contextmenu(self, state: bool = True):
        self.setShortcutVisibleInContextMenu(state)

    usage_count = core.Property(int, get_usage_count)


class Action(ActionMixin, gui.QAction):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    action = Action(text="This is a test", shortcut=None)
