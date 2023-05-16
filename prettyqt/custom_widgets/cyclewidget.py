from __future__ import annotations

from collections.abc import Iterable

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtWidgets


class CycleWidget(widgets.ListWidget):
    current_item_changed = core.Signal(QtWidgets.QListWidgetItem)

    def __init__(
        self,
        items: Iterable,
        item_size: QtCore.QSize,
        align=QtCore.Qt.AlignmentFlag.AlignCenter,
        parent=None,
    ):
        super().__init__(parent=parent)
        self.item_size = item_size
        self.align = align

        self.up_button = widgets.ToolButton(parent=self, clicked=self.scroll_up)
        self.up_button.set_icon("mdi.arrow-up-bold-outline")
        self.down_button = widgets.ToolButton(parent=self, clicked=self.scroll_down)
        self.down_button.set_icon("mdi.arrow-down-bold-outline")
        self.origin_items = list(items)

        self.visible_number = 5

        self.setItems(items)

        self.set_vertical_scroll_mode("pixel")
        self.set_scrollbar_smooth(True, animation_duration=250)
        self.v_scrollbar.setVisible(False)
        self.set_viewport_margins(0)
        self.setFixedSize(item_size.width() + 8, item_size.height() * self.visible_number)

        self.set_scrollbar_policy("always_off")
        self.up_button.hide()
        self.down_button.hide()
        self.itemClicked.connect(self._on_item_clicked)

    def setItems(self, items: list):
        self.clear()
        self._create_items(items)

    def _create_items(self, items: list):
        N = len(items)
        self.is_cycle = N > self.visible_number

        if self.is_cycle:
            for _ in range(2):
                self._add_column_items(items)

            self._current_index = len(items)
            super().scrollToItem(
                self.item(self.currentIndex() - self.visible_number // 2),
                widgets.ListWidget.ScrollHint.PositionAtTop,
            )
        else:
            n = self.visible_number // 2  # add empty items to enable scrolling

            self._add_column_items([""] * n, True)
            self._add_column_items(items)
            self._add_column_items([""] * n, True)

            self._current_index = n

    def _add_column_items(self, items, disabled: bool = False):
        for i in items:
            item = widgets.ListWidgetItem(str(i), self)
            item.setSizeHint(self.item_size)
            item.setTextAlignment(self.align | QtCore.Qt.AlignmentFlag.AlignVCenter)
            if disabled:
                item.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)

            self.addItem(item)

    def _on_item_clicked(self, item):
        self.setCurrentIndex(self.row(item))
        self.scrollToItem(self.currentItem())

    def setSelectedItem(self, text: str):
        items = self.findItems(text, QtCore.Qt.MatchFlag.MatchExactly)
        if not items:
            return

        idx = self.row(items[1]) if len(items) >= 2 else self.row(items[0])
        self.setCurrentIndex(idx)
        super().scrollToItem(
            self.currentItem(), widgets.ListWidget.ScrollHint.PositionAtCenter
        )

    def scrollToItem(
        self,
        item: QtWidgets.QListWidgetItem,
        hint=widgets.ListWidget.ScrollHint.PositionAtCenter,
    ):
        index = self.row(item)
        y = item.sizeHint().height() * (index - self.visible_number // 2)
        self.v_scrollbar.scroll_to(y)
        self.clearSelection()
        item.setSelected(False)

        self.current_item_changed.emit(item)

    def wheelEvent(self, e):
        if e.angleDelta().y() < 0:
            self.scroll_down()
        else:
            self.scroll_up()

    def scroll_down(self):
        """Scroll down an item."""
        self.setCurrentIndex(self.currentIndex() + 1)
        self.scrollToItem(self.currentItem())

    def scroll_up(self):
        """Scroll up an item."""
        self.setCurrentIndex(self.currentIndex() - 1)
        self.scrollToItem(self.currentItem())

    def enterEvent(self, e):
        self.up_button.show()
        self.down_button.show()

    def leaveEvent(self, e):
        self.up_button.hide()
        self.down_button.hide()

    def resizeEvent(self, e):
        self.up_button.resize(self.width(), 34)
        self.down_button.resize(self.width(), 34)
        self.down_button.move(0, self.height() - 34)

    def keyPressEvent(self, e):
        match e.key():
            case QtCore.Qt.Key.Key_Down:
                self.scroll_down()
            case QtCore.Qt.Key.Key_Up:
                self.scroll_up()
            case _:
                super().keyPressEvent(e)

    def currentItem(self):
        return self.item(self.currentIndex())

    def currentIndex(self):
        return self._current_index

    def setCurrentIndex(self, index: int):
        if not self.is_cycle:
            n = self.visible_number // 2
            self._current_index = max(n, min(n + len(self.origin_items) - 1, index))
            return
        N = self.count() // 2
        m = (self.visible_number + 1) // 2
        self._current_index = index

        # scroll to center to achieve circular scrolling
        if index >= self.count() - m:
            self._current_index = N + index - self.count()
            super().scrollToItem(
                self.item(self.currentIndex() - 1), self.ScrollHint.PositionAtCenter
            )
        elif index <= m - 1:
            self._current_index = N + index
            super().scrollToItem(
                self.item(N + index + 1), self.ScrollHint.PositionAtCenter
            )


if __name__ == "__main__":
    app = widgets.app()
    widget = CycleWidget(["test"] * 20, QtCore.QSize(50, 50))
    print(widget.model())
    widget.show()
    app.main_loop()
