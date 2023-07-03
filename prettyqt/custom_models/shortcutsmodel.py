from __future__ import annotations

from prettyqt import constants, custom_models, gui


class WhatsThisColumn(custom_models.ColumnItem):
    name = "Whats this"
    doc = "Whats This"
    editable = True

    def get_data(self, item: gui.QShortcut, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                return item.whatsThis()

    def set_data(self, item, value, role):
        match role:
            case constants.EDIT_ROLE:
                return item.setWhatsThis(value)


class EnabledColumn(custom_models.ColumnItem):
    name = "Enabled"
    doc = "Whether shortcut is enabled."
    checkable = True

    def get_data(self, item: gui.QShortcut, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(item.isEnabled())

    def set_data(self, item, value, role):
        match role:
            case constants.CHECKSTATE_ROLE:
                item.setEnabled(not item.isEnabled())
                return True
        return False


class ShortcutColumn(custom_models.ColumnItem):
    name = "Shortcut"
    doc = "Keyboard shortcut."
    editable = True

    def get_data(self, item: gui.QShortcut, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.key().toString()
            case constants.EDIT_ROLE:
                return item.key()

    def set_data(self, item, value, role):
        match role:
            case constants.EDIT_ROLE:
                item.setKey(value)
                return True
        return False


class ContextColumn(custom_models.ColumnItem):
    name = "Context"
    doc = "Shortcut context."
    editable = True

    def get_data(self, item: gui.QShortcut, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return constants.SHORTCUT_CONTEXT.inverse[item.context()]
            case constants.EDIT_ROLE:
                return item.context()

    def set_data(self, item, value, role):
        match role:
            case constants.EDIT_ROLE:
                item.setContext(value)
                return True
        return False


class AutoRepeatColumn(custom_models.ColumnItem):
    name = "Auto-repeat"
    doc = "Auto-repeat."
    checkable = True

    def get_data(self, item: gui.QShortcut, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(item.autoRepeat())

    def set_data(self, item, value, role):
        match role:
            case constants.CHECKSTATE_ROLE:
                item.setAutoRepeat(not item.autoRepeat())


class ParentColumn(custom_models.ColumnItem):
    name = "Parent widget"
    doc = "Parent widget."

    def get_data(self, item: gui.QShortcut, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.parent().windowTitle() or item.parent().__class__.__name__


class ShortcutsModel(custom_models.ColumnTableModel):
    COLUMNS = [
        WhatsThisColumn,
        EnabledColumn,
        ShortcutColumn,
        AutoRepeatColumn,
        ContextColumn,
        ParentColumn,
    ]

    def __init__(self, shortcuts, parent=None):
        super().__init__(shortcuts, self.COLUMNS, parent=parent)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (gui.QShortcut(), *_):
                return True
            case _:
                return False


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    shortcuts = [
        gui.Shortcut("Ctrl+A", view, print, object_name="super duper"),
        gui.Shortcut("Ctrl+B", view, print, object_name="this is an shortcut"),
        gui.Shortcut("Ctrl+C", view, print, object_name="fsfsfsdfs sfd"),
        gui.Shortcut("Ctrl+D", view, print, object_name="fsfsfsdfs sfd"),
    ]
    for i in shortcuts:
        i.setWhatsThis("abc")
    model = ShortcutsModel(shortcuts, parent=view)
    view.setModel(model)
    view.set_delegate("editor")
    view.resize(640, 480)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    view.show()
    with app.debug_mode():
        app.exec()
