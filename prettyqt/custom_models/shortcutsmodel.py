from __future__ import annotations

from prettyqt import constants, custom_models, gui


COL_NAME = custom_models.ColumnItem(
    name="Name",
    doc="WhatsThis",
    label=lambda x: x.whatsThis(),
    # decoration=lambda x: x.icon(),
)

COL_ENABLED = custom_models.ColumnItem(
    name="Enabled",
    doc="Enabled",
    checkable=True,
    checkstate=lambda x: x.isEnabled(),
    set_checkstate=lambda item, value: item.setEnabled(not item.isEnabled()),
)

COL_SHORTCUT = custom_models.ColumnItem(
    name="Shortcut",
    doc="Shortcut",
    label=lambda x: x.key().toString(),
)

COL_CONTEXT = custom_models.ColumnItem(
    name="Context",
    doc="Context",
    label=lambda x: constants.SHORTCUT_CONTEXT.inverse[x.context()],
)

COL_AUTOREPEAT = custom_models.ColumnItem(
    name="AutoRepeat",
    doc="AutoRepeat",
    checkable=True,
    checkstate=lambda item: item.autoRepeat(),
    set_checkstate=lambda item, value: item.setAutoRepeat(not item.autoRepeat()),
)


COLUMNS = [
    COL_NAME,
    COL_ENABLED,
    COL_SHORTCUT,
    COL_CONTEXT,
    COL_AUTOREPEAT,
]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    shortcuts = [
        gui.Shortcut(
            "Ctrl+A",
            view,
            lambda: print("test"),
            object_name="super duper shortcut",
        ),
        gui.Shortcut(
            "Ctrl+B",
            view,
            print,
            object_name="this is an shortcut",
        ),
        # gui.Shortcut(
        #     view,
        #     object_name="another one",
        #     key="Ctrl+Alt+A",
        # ),
    ]
    for i in shortcuts:
        i.setWhatsThis("abc")
    model = custom_models.ColumnTableModel(shortcuts, COLUMNS, parent=view)
    view.setModel(model)
    view.resize(640, 480)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    view.show()
    with app.debug_mode():
        app.main_loop()
