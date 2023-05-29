from __future__ import annotations

import logging

from prettyqt import debugging, widgets
from prettyqt.custom_models import (
    logrecordmodel,
    widgetpropertiesmodel,
    widgethierarchymodel,
)
from prettyqt.custom_widgets import filtercontainer

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
        if self.model() is not None:
            self.model().disconnect()
        model = widgetpropertiesmodel.WidgetPropertiesModel(qobject, parent=self)
        model.dataChanged.connect(self.repaint)
        self.set_model(model)


class QObjectDetailsDialog(widgets.MainWindow):
    """A dialog containing information about a QObject."""

    def __init__(self, qobject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qobject = qobject

        self.propertyview = PropertyView()
        self.propertyview.set_qobject(qobject)
        propertyviewcontainer = filtercontainer.FilterContainer(self.propertyview)
        self.hierarchyview = HierarchyView()
        model = widgethierarchymodel.WidgetHierarchyModel(
            qobject, parent=self.hierarchyview
        )
        model = model.proxifier[:, 0:3]
        hierarchycontainer = filtercontainer.FilterContainer(self.hierarchyview)
        self.hierarchyview.set_model(model)
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
        self.add_dockwidget(propertyviewcontainer, window_title="Property view")
        self.add_dockwidget(logtable, window_title="Log")
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
    with widgets.VBoxLayout.create(widget) as layout:
        with layout.get_sub_layout("splitter", orientation="horizontal") as layout:
            layout += widgets.PlainTextEdit("upper left")
            layout += widgets.PlainTextEdit("upper middle")
            with layout.get_sub_layout("splitter", orientation="vertical") as layout:
                layout += widgets.PlainTextEdit("upper right")
                layout += widgets.PlainTextEdit("middle right")
                with layout.get_sub_layout("horizontal") as layout:
                    layout += widgets.PlainTextEdit("upper right")
                    layout += widgets.PlainTextEdit("middle right")
                    button = layout.add(widgets.PushButton("test"))
        with layout.get_sub_layout("horizontal") as layout:
            layout += widgets.PlainTextEdit("lower left")
            layout += widgets.PlainTextEdit("lower right")

    button.clicked.connect(lambda: widget.layout().addWidget(widgets.Label("test")))
    with app.debug_mode():
        wnd = QObjectDetailsDialog(widget)
        wnd.show()
        app.main_loop()
