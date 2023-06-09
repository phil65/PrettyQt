from __future__ import annotations

import logging
from prettyqt import constants, core, widgets
from prettyqt.qt import QtWidgets

logger = logging.getLogger(__name__)


class FilterContainer(widgets.Widget):
    def __init__(
        self,
        parent: widgets.TableView | widgets.TreeView,
        object_name="filter_container",
        **kwargs,
    ):
        super().__init__(object_name=object_name, **kwargs)
        self.set_layout("vertical")
        self._proxies = []
        self.set_margin(0)
        self.spacer = widgets.Widget()
        self._filter_layout = widgets.HBoxLayout(margin=0, spacing=1)
        self._filter_layout.add(self.spacer)
        model = parent.model()
        self._parent = parent
        self._filter_scrollarea = widgets.ScrollArea(
            horizontal_scroll_bar_policy="always_off", frame_shape="no_frame"
        )
        self._filter_scrollarea.set_size_policy("expanding", "minimum")
        self._topline_layout = widgets.HBoxLayout(margin=0, spacing=0)
        self._topline_layout.add(self.spacer)
        self._topline_layout.add(self._filter_scrollarea)
        parent.h_header.sectionResized.connect(self._on_section_resize)
        for i in range(parent.h_header.count()):
            if model.get_column_type(i) is bool:
                widget = widgets.ComboBox(margin=0, object_name=f"filter_combo_{i}")
                widget.add_items(
                    {None: "Show all", True: "Show True", False: "Show False"}
                )
                proxy = model.proxifier.get_proxy(
                    "value_filter",
                    recursive_filtering_enabled=True,
                    filter_key_column=i,
                    filter_role=constants.CHECKSTATE_ROLE,
                )
                widget.value_changed.connect(proxy.set_filter_value)
            else:
                widget = widgets.LineEdit(margin=0, object_name=f"filter_combo_{i}")
                proxy = model.proxifier.get_proxy(
                    "sort_filter", recursive_filtering_enabled=True, filter_key_column=i
                )
                widget.value_changed.connect(proxy.setFilterFixedString)
                title = model.headerData(i, constants.HORIZONTAL, constants.DISPLAY_ROLE)
                widget.setPlaceholderText(f"Filter {title}...")
            self._proxies.append(proxy)
            self._filter_layout.add(widget)
            model = proxy
            widget.setFixedWidth(parent.h_header.sectionSize(i))
        if isinstance(self._parent, QtWidgets.QTableView):
            self.spacer.setFixedWidth(self._parent.v_header.width())
        else:
            self.spacer.hide()
        self._filter_layout.addStretch(1)
        parent.set_model(model)
        widget = widgets.Widget()
        widget.set_layout("horizontal", margin=0)
        widget.box.add(self._filter_layout)
        self._filter_scrollarea.set_widget(widget)
        self._filter_scrollarea.setFixedHeight(30)
        parent.h_scrollbar.valueChanged.connect(
            self._filter_scrollarea.h_scrollbar.setValue
        )
        self._filter_scrollarea.h_scrollbar.setMinimum(parent.h_scrollbar.minimum())
        self._filter_scrollarea.h_scrollbar.setMaximum(parent.h_scrollbar.maximum())
        parent.set_horizontal_scroll_mode("pixel")

        self.box.add(self._topline_layout)
        self.box.add(parent)

    def _on_section_resize(self, index, new_size, old_size):
        # perhaps check header.sectionPosition() and sectionSize() for correct pos?
        # logger.debug(f"resizing for index {index}")
        widget = self._filter_layout[index]
        widget.setFixedWidth(new_size)
        if isinstance(self._parent, QtWidgets.QTableView):
            self.spacer.setFixedWidth(self._parent.v_header.width())
        else:
            self.spacer.hide()
        self._filter_scrollarea.setFixedWidth(self._parent.viewport().width())

    def set_filter_case_sensitivity(self, sensitivity):
        for proxy in self._proxies:
            proxy.setFilterCaseSensitivity(sensitivity)

    def set_filter_mode(self, mode: core.sortfilterproxymodel.FilterModeStr):
        for proxy in self._proxies:
            if isinstance(proxy, core.SortFilterProxyModel):
                proxy.set_filter_mode(mode)


if __name__ == "__main__":
    from prettyqt.custom_models import widgetpropertiesmodel

    app = widgets.app()
    view = widgets.TableView()

    model = widgetpropertiesmodel.WidgetPropertiesModel(view.h_header, parent=view)
    # model = model.proxifier[:, 0:3]
    view.set_selection_behavior("rows")
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("variant", column=1)

    view.setModel(model)
    view.resize(640, 480)
    view.set_selection_behavior("rows")
    view.adapt_sizes()
    w = FilterContainer(view)
    w.show()
    with app.debug_mode():
        app.main_loop()
