from __future__ import annotations

import logging
from prettyqt import constants, core, widgets

logger = logging.getLogger(__name__)


class FilterHeader(widgets.HeaderView):
    def __init__(self, parent: widgets.TableView):
        self._editors_visible = False
        self._editors = []
        self._proxies = []
        self._padding = 6
        super().__init__(constants.HORIZONTAL, parent)
        self.setStretchLastSection(True)
        # self.setResizeMode(QHeaderView.Stretch)
        self.setDefaultAlignment(constants.ALIGN_CENTER_LEFT)
        # self.setSortIndicatorShown(False)
        self.sectionResized.connect(self.adjust_positions)
        parent.h_scrollbar.valueChanged.connect(self.adjust_positions)
        parent.model_changed.connect(self.update_filter_boxes)
        self.sectionResized.connect(self.adjust_positions)
        self.update_filter_boxes()
        self.update_geometries()

    def editors_visible(self):
        return self._editors_visible

    def set_editors_visible(self, visible: bool):
        self._editors_visible = visible
        for editor in self._editors:
            editor.setVisible(visible)
        self.updateGeometries()

    def update_filter_boxes(self):
        # TODO: deal with column changes by connecting to Model signals.
        # That way we wouldnt have to update all editors on change.
        while self._editors:
            editor = self._editors.pop()
            editor.deleteLater()
        self.create_editors(self.parent())
        self.adjust_positions()

    def create_editors(self, parent):
        # using parent model here bc we cant guarantee that we are already set to view.
        model = self.parent().model()
        with self.parent().signals_blocked():
            for i in range(model.columnCount()):
                if model.get_column_type(i) is bool:
                    widget = widgets.ComboBox(
                        margin=0, object_name=f"filter_combo_{i}", parent=self
                    )
                    widget.add_items(
                        {None: "Show all", True: "Show True", False: "Show False"}
                    )
                    proxy = parent.proxifier.get_proxy(
                        "value_filter",
                        recursive_filtering_enabled=True,
                        filter_key_column=i,
                        filter_role=constants.CHECKSTATE_ROLE,
                    )
                    widget.value_changed.connect(proxy.set_filter_value)
                else:
                    widget = widgets.LineEdit(
                        margin=0, object_name=f"filter_combo_{i}", parent=self
                    )
                    proxy = parent.proxifier.get_proxy(
                        "sort_filter",
                        recursive_filtering_enabled=True,
                        filter_key_column=i,
                    )
                    widget.value_changed.connect(proxy.setFilterFixedString)
                    title = model.headerData(
                        i, constants.HORIZONTAL, constants.DISPLAY_ROLE
                    )
                    widget.setPlaceholderText(f"Filter {title}...")
                widget.show()
                self._proxies.append(proxy)
                self._editors.append(widget)

    def sizeHint(self):
        size = super().sizeHint()
        if self._editors:
            height = self._editors[0].sizeHint().height()
            size.setHeight(size.height() + height + self._padding)
        return size

    def updateGeometries(self):
        if self._editors:
            height = self._editors[0].sizeHint().height()
            self.setViewportMargins(0, 0, 0, height + self._padding)
        else:
            self.setViewportMargins(0, 0, 0, 0)
        super().updateGeometries()
        self.adjust_positions()

    def adjust_positions(self):
        for index, editor in enumerate(self._editors):
            height = editor.sizeHint().height()
            compensate_y = 0
            compensate_x = 0
            match editor:
                case widgets.QComboBox():
                    compensate_y = +2
                case widgets.QPushButton():
                    compensate_y = -1
                case widgets.QCheckBox():
                    compensate_y = 4
                    compensate_x = 4
                case widgets.QWidget():
                    compensate_y = -1
            editor.move(
                self.sectionPosition(index) - self.offset() + 1 + compensate_x,
                height + (self._padding // 2) + compensate_y,
            )
            editor.resize(self.sectionSize(index), height)

    def set_filter_case_sensitivity(self, sensitivity):
        for proxy in self._proxies:
            proxy.setFilterCaseSensitivity(sensitivity)

    def set_filter_mode(self, mode: core.sortfilterproxymodel.FilterModeStr):
        for proxy in self._proxies:
            if isinstance(proxy, core.SortFilterProxyModel):
                proxy.set_filter_mode(mode)

    def clear_filters(self):
        for editor in self._editors:
            editor.clear()

    editors_visible = core.Property(bool, editors_visible, set_editors_visible)


if __name__ == "__main__":
    from prettyqt.custom_models import widgetpropertiesmodel

    app = widgets.app()
    with app.debug_mode():
        view = widgets.TableView()

        model = widgetpropertiesmodel.WidgetPropertiesModel(view, parent=view)
        # model = model.proxifier[:, 0:3]
        view.set_selection_behavior("rows")
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("variant", column=1)

        view.setModel(model)
        view.resize(640, 480)
        view.set_selection_behavior("rows")
        view.adapt_sizes()
        header = FilterHeader(parent=view)
        view.setHorizontalHeader(header)
        # view.h_header.update_filter_boxes()
        view.h_header.visible_editors = True
        view.show()
        with app.debug_mode():
            app.main_loop()
