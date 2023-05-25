from __future__ import annotations

import logging
from prettyqt import core, constants, widgets
from prettyqt.qt import QtWidgets

logger = logging.getLogger(__name__)


class LineEditFilterContainer(widgets.Widget):
    def __init__(self, parent: widgets.TableView | widgets.TreeView, **kwargs):
        super().__init__(**kwargs)
        self.set_layout("vertical")
        self._proxies = []
        self.set_margin(0)
        self.spacer = widgets.Widget()
        self._lineedit_layout = widgets.HBoxLayout(margin=0, spacing=1)
        self._lineedit_layout.add(self.spacer)
        model = parent.model()
        self._parent = parent
        self._lineedit_scrollarea = widgets.ScrollArea(
            horizontal_scroll_bar_policy="always_off", frame_shape="no_frame"
        )
        self._topline_layout = widgets.HBoxLayout(margin=0, spacing=0)
        self._lineedit_scrollarea.set_size_policy("expanding", "minimum")
        self._topline_layout.add(self.spacer)
        self._topline_layout.add(self._lineedit_scrollarea)
        parent.h_header.sectionResized.connect(self._resize_lineedits)
        for i in range(parent.h_header.count()):
            lineedit = widgets.LineEdit(margin=0)
            proxy = core.SortFilterProxyModel(self, recursive_filtering_enabled=True)
            self._proxies.append(proxy)
            proxy.setSourceModel(model)
            proxy.setFilterKeyColumn(i)
            lineedit.value_changed.connect(proxy.setFilterFixedString)
            self._lineedit_layout.add(lineedit)
            model = proxy
            lineedit.setFixedWidth(parent.h_header.sectionSize(i))
            title = model.headerData(i, constants.HORIZONTAL, constants.DISPLAY_ROLE)
            lineedit.setPlaceholderText(f"Filter {title}...")
        if isinstance(self._parent, QtWidgets.QTableView):
            self.spacer.setFixedWidth(self._parent.v_header.width())
        else:
            self.spacer.hide()
        self._lineedit_layout.addStretch(1)
        parent.set_model(model)
        widget = widgets.Widget()
        widget.set_layout("horizontal", margin=0)
        widget.box.add(self._lineedit_layout)
        self._lineedit_scrollarea.set_widget(widget)
        self._lineedit_scrollarea.setFixedHeight(30)
        parent.h_scrollbar.valueChanged.connect(
            self._lineedit_scrollarea.h_scrollbar.setValue
        )
        self._lineedit_scrollarea.h_scrollbar.setMinimum(parent.h_scrollbar.minimum())
        self._lineedit_scrollarea.h_scrollbar.setMaximum(parent.h_scrollbar.maximum())
        parent.set_horizontal_scroll_mode("pixel")

        self.box.add(self._topline_layout)
        self.box.add(parent)

    def _resize_lineedits(self, index, old_size, new_size):
        # perhaps check header.sectionPosition() and sectionSize() for correct pos?
        logger.debug(f"resizing for index {index}")
        self._lineedit_layout[index].setFixedWidth(new_size)
        self.spacer.setFixedWidth(self._parent.v_header.width())
        self._lineedit_scrollarea.setFixedWidth(self._parent.viewport().width())

    def set_filter_case_sensitivity(self, sensitivity):
        for proxy in self._proxies:
            proxy.setFilterCaseSensitivity(sensitivity)


if __name__ == "__main__":
    from prettyqt.custom_models import widgetpropertiesmodel

    app = widgets.app()
    view = widgets.TableView()

    model = widgetpropertiesmodel.WidgetPropertiesModel(view.h_header, parent=view)
    model = model.proxifier[:, 0:3]
    view.set_selection_behavior("rows")
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("variant", column=1)

    view.setModel(model)
    view.resize(640, 480)
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    w = LineEditFilterContainer(view)
    w.show()
    with app.debug_mode():
        app.main_loop()
