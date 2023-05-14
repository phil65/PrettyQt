from __future__ import annotations

from prettyqt import custom_models, gui


COL_NAME = custom_models.ColumnItem(
    name="Name",
    doc="Action name",
    label=lambda x: x.text(),
    # decoration=lambda x: x.icon(),
)

COL_DESCRIPTION = custom_models.ColumnItem(
    name="Description",
    doc="Description",
    label=lambda x: x.toolTip(),
)

COL_SHORTCUT = custom_models.ColumnItem(
    name="Shortcut",
    doc="Shortcut",
    label=lambda x: x.shortcut().toString(),
)

COL_PRIORITY = custom_models.ColumnItem(
    name="Priority",
    doc="Priority",
    label=lambda x: gui.action.PRIORITIES.inverse[x.priority()],
)

COL_CHECKSTATE = custom_models.ColumnItem(
    name="Checkstate",
    doc="Checkstate",
    checkstate=lambda x: x.isChecked(),
)

COL_USAGE_COUNT = custom_models.ColumnItem(
    name="Usage count",
    doc="Usage count",
    label=lambda x: x.usage_count if hasattr(x, "usage_count") else 0,
)


COLUMNS = [
    COL_NAME,
    COL_DESCRIPTION,
    COL_SHORTCUT,
    COL_PRIORITY,
    COL_CHECKSTATE,
    COL_USAGE_COUNT,
]


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
    model = custom_models.ColumnTableModel(actions, COLUMNS, parent=view)
    view.setModel(model)
    view.resize(640, 480)
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    view.show()
    app.main_loop()
