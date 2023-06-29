from __future__ import annotations

from typing import Any

from collections.abc import Generator

from prettyqt import constants, core, gui, widgets


# Subclass Delegate to increase item height
class SizeHintDelegate(widgets.StyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(20)
        return size


class MultiComboBox(widgets.ComboBox):
    selectionChanged = core.Signal(list)

    def __init__(self, parent: widgets.QWidget | None = None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.setItemDelegate(SizeHintDelegate())

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self._close_on_lineedit_click = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

        self.addItem("Show/Hide All", isChecked=True)

        self.model().itemChanged.connect(self._update_selection)
        self.model().dataChanged.connect(self._update_text)
        self.model().dataChanged.connect(self._emit_current_data)

    def _emit_current_data(self):
        self.selectionChanged.emit(self.currentData())

    def _update_selection(self, item: gui.QStandardItem):
        if item.index().row() == 0:
            state = item.checkState()
            with self.model().change_layout():
                for item in self.get_model_items():
                    item.setCheckState(state)

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

        if source == self.view().viewport():
            if event.type() == core.QEvent.Type.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().itemFromIndex(index)
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
        texts = [item.text() for item in self.get_model_items() if item.is_checked()]
        text = ", ".join(texts)
        # Compute elided text (with "...")
        metrics = gui.FontMetrics(self.lineEdit().font())
        text = metrics.elided_text(text, "right", self.lineEdit().width())
        self.lineEdit().setText(text)

    def addItem(self, text: str, data: Any = None, checked: bool = False, **kwargs):
        item = gui.StandardItem()
        item.setText(text)
        item.setData(text if data is None else data, constants.USER_ROLE)
        item.setFlags(constants.IS_ENABLED | constants.IS_CHECKABLE)
        item.set_checkstate(checked)
        self.model().appendRow(item)

    def addItems(
        self,
        items: list[str | tuple[str, Any]],
        all_checked: bool = False,
    ):
        for item in items:
            data = item[1] if isinstance(item, tuple) else item
            self.addItem(item, data, all_checked=all_checked)

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

    def get_model_items(self) -> Generator[gui.QStandardItem, None, None]:
        for i in range(1, self.model().rowCount()):
            yield self.model().item(i)

    def set_value(self, items: list[Any]):
        for item in self.get_model_items():
            if item.data(constants.USER_ROLE) in items:
                item.setChecked(True)

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
