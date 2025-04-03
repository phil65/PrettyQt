from __future__ import annotations

from collections.abc import Sequence
import logging
from typing import ClassVar

from prettyqt import constants, core, gui, itemmodels


logger = logging.getLogger(__name__)


class NameColumn(itemmodels.ColumnItem):
    name = "Name"
    doc = "Action name"
    editable = True

    def get_data(
        self,
        item: gui.QAction,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                return item.text()
            case constants.DECORATION_ROLE:
                return item.icon()

    def set_data(
        self,
        item: gui.QAction,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ):
        match role:
            case constants.EDIT_ROLE:
                item.setText(value)
                return True


class ToolTipColumn(itemmodels.ColumnItem):
    name = "ToolTip"
    doc = "ToolTip"
    editable = True

    def get_data(
        self,
        item: gui.QAction,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                return item.toolTip()

    def set_data(
        self,
        item: gui.QAction,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ):
        match role:
            case constants.EDIT_ROLE:
                item.setToolTip(value)
                return True


class ShortcutColumn(itemmodels.ColumnItem):
    name = "Shortcut"
    editable = True

    def get_data(
        self,
        item: gui.QAction,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role:
            case constants.DISPLAY_ROLE:
                return item.shortcut().toString()
            case constants.EDIT_ROLE:
                return item.shortcut()

    def set_data(
        self,
        item: gui.QAction,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ):
        match role:
            case constants.EDIT_ROLE:
                item.setShortcut(value)
                return True


class PriorityColumn(itemmodels.ColumnItem):
    name = "Priority"
    editable = True

    def get_data(
        self,
        item: gui.QAction,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        match role:
            case constants.DISPLAY_ROLE:
                return gui.action.PRIORITIES.inverse[item.priority()]
            case constants.EDIT_ROLE:
                return item.priority()

    def set_data(
        self,
        item: gui.QAction,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ):
        match role:
            case constants.EDIT_ROLE:
                item.setPriority(value)
                return True


class CheckStateColumn(itemmodels.ColumnItem):
    name = "CheckState"

    def get_data(
        self,
        item: gui.QAction,
        role: constants.ItemDataRole = constants.CHECKSTATE_ROLE,
    ):
        match role:
            case constants.CHECKSTATE_ROLE:
                return (
                    self.to_checkstate(item.isChecked()) if item.isCheckable() else None
                )
        return None

    def set_data(
        self,
        item: gui.QAction,
        value,
        role: constants.ItemDataRole = constants.CHECKSTATE_ROLE,
    ):
        match role:
            case constants.CHECKSTATE_ROLE:
                item.setChecked(not item.isChecked())
                return True
        return False

    def get_flags(self, item):
        default = constants.IS_SELECTABLE | constants.IS_ENABLED
        return default | constants.IS_CHECKABLE if item.isCheckable() else default


class UsageCountColumn(itemmodels.ColumnItem):
    name = "Usage count"

    def get_data(
        self, item: gui.QAction, role: constants.ItemDataRole = constants.DISPLAY_ROLE
    ):
        match role:
            case constants.DISPLAY_ROLE if hasattr(item, "usage_count"):
                return item.usage_count


class ActionsModel(itemmodels.ColumnTableModel):
    """Table model to display a list of QActions.

    All properties of the Action can be edited.
    """

    SUPPORTS = Sequence[gui.QAction]
    COLUMNS: ClassVar = [
        NameColumn,
        ToolTipColumn,
        ShortcutColumn,
        CheckStateColumn,
        PriorityColumn,
        UsageCountColumn,
    ]

    def __init__(self, actions: list[gui.QAction], parent: core.QObject | None = None):
        super().__init__(actions, self.COLUMNS, parent=parent)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (gui.QAction(), *_):
                return True
            case _:
                return False


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    actions = [
        gui.Action(
            text="Some nice Qt Action",
            shortcut="Ctrl+A",
            tool_tip="wonderful tooltip.",
            icon="mdi.folder",
            triggered=lambda: print("test"),
        ),
        gui.Action(
            text="Another Qt action",
            shortcut="Ctrl+B",
            tool_tip="wonderful tooltip.",
            icon="mdi.folder-outline",
        ),
        gui.Action(
            text="...and another one",
            shortcut="Ctrl+Alt+A",
            tool_tip="wonderful tooltip.",
            icon="mdi.information",
            checkable=True,
        ),
        gui.Action(
            text="....even more!",
            shortcut="Ctrl+Alt+C",
            tool_tip="wonderful tooltip.",
            icon="mdi.download",
            checkable=True,
            checked=True,
        ),
    ]
    # actions[0].trigger()
    # actions[0].trigger()
    # actions[0].trigger()
    # actions[1].trigger()
    model = ActionsModel(actions, parent=view)
    view.setModel(model)
    view.resize(640, 480)
    view.set_delegate("editor")
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    view.show()
    with app.debug_mode():
        app.exec()
