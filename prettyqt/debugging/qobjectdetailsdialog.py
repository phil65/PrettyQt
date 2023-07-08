from __future__ import annotations

import functools
import logging

from prettyqt import (
    core,
    custom_widgets,
    debugging,
    ipython,
    widgets,
)


logger = logging.getLogger(__name__)


def get_tabbed(qobject: core.QObject, parent: widgets.QWidget | None = None):
    tabwidget = widgets.TabWidget(parent=parent)
    propertyview = custom_widgets.QObjectPropertiesTableView(
        object_name="property_view", parent=tabwidget
    )
    propertyview.set_qobject(qobject)
    propertyview.h_header = custom_widgets.FilterHeader(propertyview)
    tabwidget.add_tab(propertyview, "Main")

    if hasattr(qobject, "model") and (model := qobject.model()) is not None:
        while isinstance(model, core.QAbstractProxyModel):
            view = custom_widgets.QObjectPropertiesTableView(
                object_name=f"property_view({type(model).__name__})",
                parent=tabwidget,
            )
            view.h_header = custom_widgets.FilterHeader(view)
            view.set_qobject(model)
            tabwidget.add_tab(view, type(model).__name__)
            model = model.sourceModel()
        view = custom_widgets.QObjectPropertiesTableView(
            object_name=f"property_view({type(model).__name__})",
            parent=tabwidget,
        )
        view.h_header = custom_widgets.FilterHeader(view)
        view.set_qobject(model)
        tabwidget.add_tab(view, type(model).__name__)
    # if (
    #     hasattr(qobject, "menuWidget")
    #     and (menu_widget := qobject.menuWidget()) is not None
    # ):
    #     view = cls(
    #         object_name=f"property_view({type(model).__name__})",
    #         parent=tabwidget,
    #     )
    #     view.set_qobject(menu_widget)
    #     tabwidget.add_tab(view, type(model).__name__)
    return tabwidget, propertyview


class QObjectDetailsDialog(widgets.MainWindow):
    """A dialog containing information about a QObject."""

    def __init__(
        self,
        qobject: core.QObject,
        *args,
        object_name="qobject_details_dialog",
        **kwargs,
    ):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.qobject = qobject
        self.console = ipython.InProcessIPythonWidget(self)
        self.console.push_vars(dict(app=widgets.app(), qobject=qobject))
        self.tabwidget, self.propertyview = get_tabbed(qobject)
        self.hierarchyview = custom_widgets.QObjectHierarchyTreeView()
        self.hierarchyview.set_qobject(qobject)
        sel_model = self.hierarchyview.selectionModel()
        sel_model.currentRowChanged.connect(self._current_changed)
        self.logtable = custom_widgets.LogRecordTableView()
        self.logtable.set_logger(logging.getLogger())
        w = widgets.Widget()
        w.set_layout("vertical")
        self.stalkers = []
        stalker = debugging.Stalker(qobject, log_level=logging.DEBUG)
        stalker.hook()
        self.stalkers.append(stalker)
        for widget in qobject.find_children(widgets.QWidget):
            stalker = debugging.Stalker(widget, log_level=logging.DEBUG)
            stalker.hook()
            fn = functools.partial(self._on_widget_click, widget)
            stalker.leftclick_detected.connect(fn)
            self.stalkers.append(stalker)
        # mdi_area = widgets.GraphicsView()
        # subwindow = widgets.GraphicsProxyWidget ()
        # # mdi_area.installEventFilter(self)
        # # subwindow.installEventFilter(self)
        # subwindow.set_widget(qobject)
        # mdi_area.scene().add(subwindow)
        widget = widgets.Widget()
        layout = widget.set_layout("horizontal")
        layout.add(qobject)
        self.set_central_widget(widget)
        # qobject.position_on(widget)

        self.add_dockwidget(self.hierarchyview, window_title="Hierarchy view")
        self.add_dockwidget(self.tabwidget, window_title="Property view")
        self.add_dockwidget(self.logtable, window_title="Log", visible=False)
        self.add_dockwidget(self.console, window_title="Console", visible=False)
        self.menubar = self.menuBar()
        action = widgets.mainwindow.PopupMenuAction("Docks", parent=self)
        self.menubar.add_action(action)
        self.position_on("screen", scale_ratio=0.8)

    def eventFilter(self, source, event):
        match event.type():
            case core.QEvent.Type.MouseButtonRelease:
                raise ValueError
        return False

    def closeEvent(self, event):
        for stalker in self.stalkers:
            stalker.unhook()
        super().closeEvent(event)

    def _current_changed(self, new, old):
        # logger.info(f"{new=} {old=}")
        role = self.hierarchyview.get_model(skip_proxies=True).Roles.WidgetRole
        if (qobject := self.hierarchyview.current_data(role)) is not None:
            self.propertyview.set_qobject(qobject)

    def _on_widget_click(self, widget):
        logger.info(repr(widget))
        self.hierarchyview.select_object(widget)

    @classmethod
    def setup_example(cls):
        w = widgets.PlainTextEdit()
        return cls(w)


if __name__ == "__main__":
    app = widgets.app()
    tree = widgets.TreeView()
    tree.set_model_for(dict(a=2))
    widget = debugging.example_widget()
    with app.debug_mode(log_level=logging.INFO):
        wnd = QObjectDetailsDialog(widget)
        wnd.hierarchyview.select_object(None)
        wnd.show()
        app.exec()
