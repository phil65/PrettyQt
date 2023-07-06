from __future__ import annotations

from prettyqt import itemmodels, widgets


class QObjectPropertiesTableView(widgets.TableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon("mdi.folder")
        self.set_selection_behavior("rows")
        self.setEditTriggers(self.EditTrigger.AllEditTriggers)
        self.set_delegate("editor", column=1)

    def set_qobject(self, qobject):
        if (model := self.get_model(skip_proxies=True)) is not None:
            model.unhook()
        model = itemmodels.QObjectPropertiesModel(qobject, parent=self)
        model.dataChanged.connect(self.repaint)
        self.set_model(model)


if __name__ == "__main__":
    app = widgets.app()
    w = QObjectPropertiesTableView()
    w.show()
    app.exec()
