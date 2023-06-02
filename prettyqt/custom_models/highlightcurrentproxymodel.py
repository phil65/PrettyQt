from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtGui


class HighlightCurrentProxyModel(core.IdentityProxyModel):
    ID = "highlight_current"

    def __init__(self, *args, role=constants.DISPLAY_ROLE, mode="column", **kwargs):
        self._mode = mode
        self._current_value = None
        self._data_role = constants.DISPLAY_ROLE
        self._column = None
        super().__init__(*args, **kwargs)
        parent = self.parent()
        parent.model_changed.connect(self._on_model_change)
        if sel_model := parent.selectionModel():
            sel_model.currentChanged.connect(self._on_current_change)

    def _on_model_change(self, model):
        self.parent().selectionModel().currentChanged.connect(self._on_current_change)

    def _on_current_change(self, new, old):
        with self.change_layout():
            self._current_value = new.data(constants.DISPLAY_ROLE)
            self._column = new.column()

    def data(self, index, role=constants.DISPLAY_ROLE):
        if role == constants.BACKGROUND_ROLE:
            if index.data(self._data_role) == self._current_value:
                if index.column() == self._column or self._mode == "all":
                    return QtGui.QColor("red")
        return super().data(index, role)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    table = widgets.TableView()
    table.set_model(["a", "b", "c", "d", "a"])
    table.model().setParent(table)
    model = table.model().proxifier.get_proxy("highlight_current")
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.main_loop()
