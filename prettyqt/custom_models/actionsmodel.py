from __future__ import annotations

from prettyqt import constants, custom_models, gui


class NameColumn(custom_models.ColumnItem):
    name = "Name"
    doc = "Action name"
    editable = True

    def get_data(self, item: gui.QAction, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.text()

    def set_data(self, item: gui.QAction, value, role: constants.ItemDataRole):
        match role:
            case constants.USER_ROLE | constants.EDIT_ROLE:
                item.setText(value)
                return True


class ToolTipColumn(custom_models.ColumnItem):
    name = "ToolTip"
    doc = "ToolTip"
    editable = True

    def get_data(self, item: gui.QAction, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.toolTip()

    def set_data(self, item: gui.QAction, value, role: constants.ItemDataRole):
        match role:
            case constants.USER_ROLE | constants.EDIT_ROLE:
                item.setToolTip(value)
                return True


class ShortcutColumn(custom_models.ColumnItem):
    name = "Shortcut"
    editable = True

    def get_data(self, item: gui.QAction, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.shortcut().toString()
            case constants.USER_ROLE | constants.EDIT_ROLE:
                return item.shortcut()

    def set_data(self, item: gui.QAction, value, role: constants.ItemDataRole):
        match role:
            case constants.USER_ROLE | constants.EDIT_ROLE:
                item.setShortcut(value)
                return True


class PriorityColumn(custom_models.ColumnItem):
    name = "Priority"
    editable = True

    def get_data(self, item: gui.QAction, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return gui.action.PRIORITIES.inverse[item.priority()]
            case constants.USER_ROLE:
                return item.priority()

    def set_data(self, item: gui.QAction, value, role: constants.ItemDataRole):
        match role:
            case constants.USER_ROLE:
                item.setPriority(value)
                return True


class CheckStateColumn(custom_models.ColumnItem):
    name = "CheckState"

    def get_data(self, item: gui.QAction, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                return item.isChecked()

    def set_data(self, item: gui.QAction, value, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                item.setChecked(value)
                return True


class UsageCountColumn(custom_models.ColumnItem):
    name = "Usage count"

    def get_data(self, item: gui.QAction, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE if hasattr(item, "usage_count"):
                return item.usage_count


class ActionsModel(custom_models.ColumnTableModel):
    COLUMNS = [
        NameColumn,
        ToolTipColumn,
        ShortcutColumn,
        PriorityColumn,
        CheckStateColumn,
        UsageCountColumn,
    ]

    def __init__(self, actions, parent=None):
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
            text="super duper action",
            shortcut="Ctrl+A",
            tool_tip="some Tooltip text",
            icon="mdi.folder",
            triggered=lambda: print("test"),
        ),
        gui.Action(
            text="this is an action",
            shortcut="Ctrl+B",
            tool_tip="Tooltip",
            icon="mdi.folder-outline",
            checked=True,
            checkable=True,
        ),
        gui.Action(
            text="another one",
            shortcut="Ctrl+Alt+A",
            tool_tip="Some longer tool_tippp",
            icon="mdi.folder",
        ),
        gui.Action(text="a", shortcut="Ctrl+A", tool_tip="Tooltip", icon="mdi.folder"),
    ]
    model = ActionsModel(actions, parent=view)
    view.setModel(model)
    view.resize(640, 480)
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    view.show()
    with app.debug_mode():
        app.main_loop()
