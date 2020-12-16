from typing import Callable, Literal, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import constants, core, gui
from prettyqt.utils import InvalidParamError, bidict, helpers, prettyprinter


PRIORITIES = bidict(
    low=QtWidgets.QAction.LowPriority,
    normal=QtWidgets.QAction.NormalPriority,
    high=QtWidgets.QAction.HighPriority,
)

PriorityStr = Literal["low", "normal", "high"]

ROLES = bidict(
    none=QtWidgets.QAction.NoRole,
    text_heuristic=QtWidgets.QAction.TextHeuristicRole,
    application_specific=QtWidgets.QAction.ApplicationSpecificRole,
    about_qt=QtWidgets.QAction.AboutQtRole,
    about=QtWidgets.QAction.AboutRole,
    preferences=QtWidgets.QAction.PreferencesRole,
    quit=QtWidgets.QAction.QuitRole,
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
        parent: Optional[QtCore.QObject] = None,
        text: str = "",
        icon: gui.icon.IconType = None,
        shortcut: Optional[str] = None,
        tooltip: str = "",
        checkable: bool = False,
        checked: bool = False,
        statustip: str = "",
        enabled: bool = True,
        callback: Optional[Callable] = None,
    ):
        super().__init__(parent)
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
        cls_name = self.__class__.__name__
        return f"{cls_name}({helpers.format_kwargs(self.serialize_fields())})"

    def serialize_fields(self):
        return dict(
            auto_repeat=self.autoRepeat(),
            text=self.text(),
            enabled=self.isEnabled(),
            visible=self.isVisible(),
            font=gui.Font(self.font()),
            shortcut=self.get_shortcut(),
            tool_tip=self.toolTip(),
            checkable=self.isCheckable(),
            checked=self.isChecked(),
            icon=gui.Icon(self.icon()) if not self.icon().isNull() else None,
            icon_text=self.iconText(),
            priority=self.get_priority(),
            icon_visible=self.isIconVisibleInMenu(),
            shortcut_visible=self.isShortcutVisibleInContextMenu(),
            menu_role=self.get_menu_role(),
            shortcut_context=self.get_shortcut_context(),
            status_tip=self.statusTip(),
            whats_this=self.whatsThis(),
            menu=self.menu(),
        )

    def __setstate__(self, state):
        self.set_text(state.get("text", ""))
        self.set_enabled(state.get("enabled", True))
        self.set_shortcut(state["shortcut"])
        self.set_tooltip(state.get("tool_tip", ""))
        self.set_statustip(state.get("status_tip", ""))
        self.set_checked(state.get("checked", False))
        self.set_priority(state["priority"])
        self.set_shortcut_context(state["shortcut_context"])
        self.set_checkable(state["checkable"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_text(self, text: str):
        self.setText(text)

    def set_enabled(self, enabled: bool = True):
        self.setEnabled(enabled)

    def set_disabled(self):
        self.setEnabled(False)

    def set_tooltip(self, text: str):
        self.setToolTip(text)

    def set_statustip(self, text: str):
        self.setStatusTip(text)

    def set_checked(self, value: bool):
        self.setChecked(value)

    def set_checkable(self, value: bool):
        self.setCheckable(value)

    def set_icon(self, icon: gui.icon.IconType):
        """Set the icon for the action.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

    def set_shortcut(self, shortcut):
        if shortcut:
            self.setShortcut(shortcut)

    def get_shortcut(self) -> Optional[gui.KeySequence]:
        shortcut = self.shortcut()
        if not shortcut:
            return None
        return gui.KeySequence(shortcut)

    def set_menu(self, menu):
        self.setMenu(menu)

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
    action = Action("This is a test")
    app.main_loop()
