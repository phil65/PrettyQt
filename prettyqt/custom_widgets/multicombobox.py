from typing import TYPE_CHECKING, Any, cast

from prettyqt import constants, core, gui, widgets


if TYPE_CHECKING:
    from collections.abc import Generator, Sequence


# Subclass Delegate to increase item height
class SizeHintDelegate(widgets.StyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(20)
        return size


class MultiComboBox(widgets.ComboBox):
    """ComboBox allowing multiple-choice selection."""

    selectionChanged = core.Signal(list)  # noqa: N815

    def __init__(self, parent: widgets.QWidget | None = None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self._model = gui.StandardItemModel(self)
        self.setModel(self._model)
        self.setEditable(True)
        line_edit = self.lineEdit()
        assert line_edit is not None
        line_edit.setReadOnly(True)
        self.setItemDelegate(SizeHintDelegate())

        # Hide and show popup when clicking the line edit
        line_edit.installEventFilter(self)
        self._close_on_lineedit_click = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

        self.addItem("Show/Hide All", checked=True)

        self._model.itemChanged.connect(self._update_selection)
        self._model.dataChanged.connect(self._update_text)
        self._model.dataChanged.connect(self._emit_current_data)

    def _emit_current_data(self):
        self.selectionChanged.emit(self.currentData())

    def _update_selection(self, item: gui.QStandardItem):
        if item.index().row() == 0:
            state = item.checkState()
            with self._model.change_layout():
                for _item in self.get_model_items():
                    _item.setCheckState(state)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self._update_text()
        super().resizeEvent(event)

    def eventFilter(self, source, event):
        if source == self.lineEdit():
            if event.type() == core.QEvent.Type.MouseButtonRelease:
                if self._close_on_lineedit_click:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if (
            source == self.view().viewport()
            and event.type() == core.QEvent.Type.MouseButtonRelease
        ):
            index = self.view().indexAt(event.position().toPoint())
            item = self._model.itemFromIndex(index)
            if isinstance(item, gui.StandardItem):
                item.toggle_checkstate()
            return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self._close_on_lineedit_click = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self._update_text()

    def timerEvent(self, event):
        # After timeout, kill timer, and re-enable click on line edit
        self.killTimer(event.timerId())
        self._close_on_lineedit_click = False

    def _update_text(self):
        line_edit = self.lineEdit()
        if line_edit is None:
            return
        texts = [item.text() for item in self.get_model_items() if item.is_checked()]
        text = ", ".join(texts)
        # Compute elided text (with "...")
        metrics = gui.FontMetrics(line_edit.font())
        text = metrics.elided_text(text, "right", line_edit.width())
        line_edit.setText(text)

    def addItem(self, text: str, data: Any = None, checked: bool = False, **kwargs):
        item = gui.StandardItem()
        item.setText(text)
        item.setData(text if data is None else data, constants.USER_ROLE)
        item.setFlags(constants.IS_ENABLED | constants.IS_CHECKABLE)
        item.set_checkstate(checked)
        self._model.appendRow([item])

    def addItems(
        self,
        items: Sequence[str | tuple[str, Any]],
        all_checked: bool = False,
    ):
        for item in items:
            text, data = item if isinstance(item, tuple) else (item, item)
            self.addItem(text, data, checked=all_checked)

    def currentData(
        self, role: constants.ItemDataRole = constants.USER_ROLE
    ) -> list[Any]:
        return [item.data(role) for item in self.get_model_items() if item.is_checked()]

    def get_current_options(self) -> list[tuple[str, Any]]:
        return [
            (item.text(), item.data(constants.USER_ROLE))
            for item in self.get_model_items()
            if item.is_checked()
        ]

    def get_model_items(self) -> Generator[gui.StandardItem]:
        for i in range(1, self._model.rowCount()):
            if (item := self._model.item(i)) is not None:
                yield cast("gui.StandardItem", item)

    def set_value(self, items: list[Any]):
        for item in self.get_model_items():
            item.set_checkstate(item.data(constants.USER_ROLE) in items)

    def get_value(self) -> list[Any]:
        return self.currentData()


if __name__ == "__main__":
    app = widgets.app()
    items = [
        "Ameglia",
        "Arcola",
        "Bagnone",
        "Bolano",
        "Carrara",
        "Casola",
        "Castelnuovo Magra",
        "Comano, località Crespiano",
        "Fivizzano",
        "Fivizzano località Pieve S. Paolo",
        "Zignago",
    ]
    combo = MultiComboBox()
    combo.addItems(items)
    combo.show()
    with app.debug_mode():
        app.exec()
