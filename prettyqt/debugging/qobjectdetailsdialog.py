from __future__ import annotations

import logging

from prettyqt import debugging, ipython, widgets
from prettyqt.custom_models import (
    logrecordmodel,
    widgetpropertiesmodel,
    widgethierarchymodel,
)
from prettyqt.custom_widgets import filtercontainer
from prettyqt.qt import QtCore, QtWidgets

logger = logging.getLogger(__name__)


class HierarchyView(widgets.TreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_indentation(10)
        self.h_header.resize_sections()
        self.setRootIsDecorated(True)


class PropertyView(widgets.TableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon("mdi.folder")
        self.set_selection_behavior("rows")
        self.setEditTriggers(self.EditTrigger.AllEditTriggers)
        self.set_delegate("variant", column=1)

    def set_qobject(self, qobject):
        if (model := self.get_model(skip_proxies=True)) is not None:
            model.unhook()
        model = widgetpropertiesmodel.WidgetPropertiesModel(qobject, parent=self)
        model.dataChanged.connect(self.repaint)
        self.set_model(model)

    @classmethod
    def get_tabbed(cls, qobject: QtCore.QObject, parent: QtWidgets.QWidget | None = None):
        tabwidget = widgets.TabWidget(parent=parent)
        propertyview = cls(object_name="property_view", parent=tabwidget)
        propertyview.set_qobject(qobject)
        propertyviewcontainer = filtercontainer.FilterContainer(propertyview)
        tabwidget.add_tab(propertyviewcontainer, "Main")
        model = qobject.model()
        if not hasattr(qobject, "model") or model is None:
            return tabwidget, propertyview
        while isinstance(model, QtCore.QAbstractProxyModel):
            view = cls(
                object_name=f"property_view({type(model).__name__})",
                parent=tabwidget,
            )
            view.set_qobject(model)
            container = filtercontainer.FilterContainer(view)
            tabwidget.add_tab(container, type(model).__name__)
            model = model.sourceModel()
        view = cls(
            object_name=f"property_view({type(model).__name__})",
            parent=tabwidget,
        )
        view.set_qobject(model)
        container = filtercontainer.FilterContainer(view)
        tabwidget.add_tab(container, type(model).__name__)
        return tabwidget, propertyview


class QObjectDetailsDialog(widgets.MainWindow):
    """A dialog containing information about a QObject."""

    def __init__(
        self,
        qobject: QtCore.QObject,
        *args,
        object_name="qobject_details_dialog",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.qobject = qobject
        self.console = ipython.InProcessIPythonWidget(self)
        tabwidget, self.propertyview = PropertyView.get_tabbed(qobject)
        self.hierarchyview = HierarchyView()
        model = widgethierarchymodel.WidgetHierarchyModel(
            qobject, parent=self.hierarchyview
        )
        model = model.proxifier[:, 0:3]
        self.hierarchyview.set_model(model)
        hierarchycontainer = filtercontainer.FilterContainer(self.hierarchyview)
        self.hierarchyview.expandAll()
        self.hierarchyview.selectionModel().currentChanged.connect(self._current_changed)

        logtable = widgets.TableView()
        model = logrecordmodel.LogRecordModel(logging.getLogger(), parent=logtable)
        w = widgets.Widget()
        w.set_layout("vertical")
        logtable.set_model(model)
        logtable.set_selection_behavior("rows")
        self.stalker = debugging.Stalker(qobject)
        self.stalker.hook()
        mdi_area = widgets.MdiArea()
        mdi_area.add_subwindow(qobject)
        self.set_central_widget(mdi_area)

        self.add_dockwidget(hierarchycontainer, window_title="Hierarchy view")
        self.add_dockwidget(tabwidget, window_title="Property view")
        self.add_dockwidget(logtable, window_title="Log")
        self.add_dockwidget(self.console, window_title="Console")
        self.position_on("screen", scale_ratio=0.8)

    def _current_changed(self, *args):
        role = self.hierarchyview.get_model(skip_proxies=True).Roles.WidgetRole
        qobject = self.hierarchyview.current_data(role)
        if qobject is None:
            return
        self.propertyview.set_qobject(qobject)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.Widget()
    tree = widgets.TreeView()
    tree.set_model(dict(a=2))
    tree.model().proxifier.get_proxy("fuzzy")
    widget = debugging.example_tree(flatten=True)
    with app.debug_mode():
        wnd = QObjectDetailsDialog(widget)
        wnd.show()
        app.main_loop()
