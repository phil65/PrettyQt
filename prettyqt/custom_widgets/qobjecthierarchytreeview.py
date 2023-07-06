from __future__ import annotations

import logging

from prettyqt import core, custom_widgets, itemmodels, widgets


logger = logging.getLogger(__name__)


class QObjectHierarchyTreeView(widgets.TreeView):
    object_selected = core.Signal(core.QObject)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_indentation(10)
        self.h_header.resize_sections()
        self.setRootIsDecorated(True)
        self.setWordWrap(True)

    def select_object(self, qobject: core.QObject):
        model = self.get_model(skip_proxies=True)
        if index := model.search_tree(qobject, model.Roles.WidgetRole):
            self.set_current_index(index[0], current=True)
            self.scroll_to(index[0])

    def set_qobject(self, qobject: core.QObject):
        model = itemmodels.WidgetHierarchyModel(qobject, parent=self)
        self.set_model(model)
        self.h_header = custom_widgets.FilterHeader(self)
        self.expandAll()


if __name__ == "__main__":
    app = widgets.app()
    test = custom_widgets.RectFEdit()
    with app.debug_mode():
        w = QObjectHierarchyTreeView()
        w.set_qobject(test)
        w.show()
        app.exec()
