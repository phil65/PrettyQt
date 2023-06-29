from __future__ import annotations

import logging

from prettyqt import constants, core, custom_widgets, widgets


logger = logging.getLogger(__name__)

BOOL_ITEMS = {
    None: "Show all",
    constants.CheckState.Checked: "Show True",
    constants.CheckState.Unchecked: "Show False",
}


class FilterHeader(widgets.HeaderView):
    def __init__(self, parent: widgets.TableView):
        self._editors_visible = False
        self._editors = []
        self._proxy = parent.proxifier.get_proxy(
            "multi_column_filter",
            recursive_filtering_enabled=True,
        )
        self._padding = 6
        super().__init__(constants.HORIZONTAL, parent)
        self.setStretchLastSection(True)
        # self.setResizeMode(QHeaderView.Stretch)
        self.setDefaultAlignment(constants.ALIGN_CENTER_LEFT)
        # self.setSortIndicatorShown(False)
        self.sectionResized.connect(self._adjust_positions)
        parent.h_scrollbar.valueChanged.connect(self._adjust_positions)
        parent.model_changed.connect(self._update_filter_boxes)
        self.sectionResized.connect(self._adjust_positions)
        self._update_filter_boxes()
        self.update_geometries()

    def editors_visible(self) -> bool:
        return self._editors_visible

    def set_editors_visible(self, visible: bool):
        self._editors_visible = visible
        for editor in self._editors:
            editor.setVisible(visible)
        self.updateGeometries()

    def _update_filter_boxes(self):
        # TODO: deal with column changes by connecting to Model signals.
        # That way we wouldnt have to update all editors on change.
        while self._editors:
            editor = self._editors.pop()
            editor.deleteLater()
        self.create_editors()
        self._adjust_positions()

    def create_editors(self):
        # using parent model here bc we cant guarantee that we are already set to view.
        parent = self.parent()
        model = parent.model()
        self._proxy.clear_filters()
        for i in range(model.columnCount()):
            typ = model.get_column_type(i)
            if typ is bool:

                def set_filter(val, i=i):
                    self._proxy.set_filter_value(i, val, constants.CHECKSTATE_ROLE)

                name = f"filter_combo_{i}"
                widget = widgets.ComboBox(margin=0, object_name=name, parent=self)
                widget.add_items(BOOL_ITEMS)
                widget.value_changed.connect(set_filter)
            elif typ in [int, float]:

                def set_filter(val, i=i):
                    self._proxy.set_filter_value(i, val)

                name = f"filter_numwidget_{i}"
                widget = custom_widgets.NumFilterWidget(
                    margin=0, object_name=name, parent=self
                )
                widget.filter_changed.connect(set_filter)
                title = model.headerData(i, constants.HORIZONTAL, constants.DISPLAY_ROLE)
                widget.lineedit.setPlaceholderText(f"Filter {title}...")
            elif typ is str:

                def set_filter(val, i=i):
                    self._proxy.set_filter_value(i, val)

                name = f"filter_lineedit_{i}"
                widget = widgets.LineEdit(margin=0, object_name=name, parent=self)
                widget.value_changed.connect(set_filter)
                title = model.headerData(i, constants.HORIZONTAL, constants.DISPLAY_ROLE)
                widget.setPlaceholderText(f"Filter {title}...")
            else:
                widget = widgets.Widget()
            widget.show()
            self._editors.append(widget)

    def sizeHint(self) -> core.QSize:
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
        self._adjust_positions()

    def _adjust_positions(self):
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

    def set_filter_case_sensitive(self, value: bool):
        self._proxy.set_filter_case_sensitive(value)

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
        # view.h_header._update_filter_boxes()
        view.h_header.visible_editors = True
        view.show()
        with app.debug_mode():
            app.exec()
            print(view.h_header._proxy._filters)
