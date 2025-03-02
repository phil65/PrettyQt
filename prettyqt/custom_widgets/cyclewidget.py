from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import constants, core, widgets


if TYPE_CHECKING:
    from collections.abc import Iterable


class CycleWidget(widgets.ListWidget):
    current_item_changed = core.Signal(widgets.QListWidgetItem)

    def __init__(
        self,
        items: Iterable,
        item_size: core.QSize,
        align=constants.AlignmentFlag.AlignCenter,
        parent=None,
    ):
        super().__init__(parent=parent)
        self.item_size = item_size
        self.align = align

        self.up_button = widgets.ToolButton(
            parent=self, clicked=self.scroll_up, visible=False
        )
        self.up_button.set_icon("mdi.arrow-up-bold-outline")
        self.down_button = widgets.ToolButton(
            parent=self, clicked=self.scroll_down, visible=False
        )
        self.down_button.set_icon("mdi.arrow-down-bold-outline")
        self.origin_items = list(items)
        self.visible_number = 5
        self.setItems(items)
        self.set_vertical_scroll_mode("pixel")
        self.set_scrollbar_smooth(True, animation_duration=250)
        self.v_scrollbar.hide()
        self.set_viewport_margins(0)
        self.setFixedSize(item_size.width() + 8, item_size.height() * self.visible_number)

        self.set_scrollbar_policy("always_off")
        self.itemClicked.connect(self._on_item_clicked)

    def setItems(self, items: list[str]):
        self.clear()
        self._create_items(items)

    def _create_items(self, items: list[str]):
        N = len(items)  # noqa: N806
        self.is_cycle = self.visible_number < N

        if self.is_cycle:
            for _ in range(2):
                self._add_column_items(items)

            self._current_index = len(items)
            item = self.item(self.currentIndex() - self.visible_number // 2)
            super().scroll_to_item(item, "position_at_top")
        else:
            n = self.visible_number // 2  # add empty items to enable scrolling

            self._add_column_items([""] * n, True)
            self._add_column_items(items)
            self._add_column_items([""] * n, True)

            self._current_index = n

    def _add_column_items(self, items: list[str], disabled: bool = False):
        for i in items:
            item = widgets.ListWidgetItem(str(i), self)
            item.setSizeHint(self.item_size)
            item.setTextAlignment(self.align | constants.AlignmentFlag.AlignVCenter)
            if disabled:
                item.setFlags(constants.ItemFlag.NoItemFlags)

            self.addItem(item)

    def _on_item_clicked(self, item: widgets.ListWidgetItem):
        self.setCurrentIndex(self.row(item))
        self.scrollToItem(self.currentItem())

    def setSelectedItem(self, text: str):
        items = self.findItems(text, constants.MatchFlag.MatchExactly)
        if not items:
            return

        idx = self.row(items[1]) if len(items) >= 2 else self.row(items[0])  # noqa: PLR2004
        self.setCurrentIndex(idx)
        super().scroll_to_item(self.currentItem(), "position_at_center")

    def scrollToItem(
        self,
        item: widgets.QListWidgetItem,
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
            case constants.Key.Key_Down:
                self.scroll_down()
            case constants.Key.Key_Up:
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
        N = self.count() // 2  # noqa: N806
        m = (self.visible_number + 1) // 2
        self._current_index = index
        # scroll to center to achieve circular scrolling
        if index >= self.count() - m:
            self._current_index = N + index - self.count()
            item = self.item(self.currentIndex() - 1)
        elif index <= m - 1:
            self._current_index = N + index
            item = self.item(N + index + 1)
        else:
            return
        super().scrollToItem(item, self.ScrollHint.PositionAtCenter)


if __name__ == "__main__":
    app = widgets.app()
    widget = CycleWidget([str(i) for i in range(30)], core.QSize(50, 50))
    widget.show()
    app.exec()
