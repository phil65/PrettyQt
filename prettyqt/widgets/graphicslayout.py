from __future__ import annotations

from collections.abc import Iterator

from prettyqt import widgets
from prettyqt.utils import listdelegators


class GraphicsLayoutMixin(widgets.GraphicsLayoutItemMixin):
    def __getitem__(
        self, index: int | slice
    ) -> widgets.QGraphicsItem | listdelegators.ListDelegator[widgets.QGraphicsItem]:
        match index:
            case int():
                if index >= self.count():
                    raise IndexError(index)
                layoutitem = self.itemAt(index)
                return layoutitem.graphicsItem()
            case slice():
                stop = index.stop or self.count()
                rng = range(index.start or 0, stop, index.step or 1)
                items = [self.itemAt(i).graphicsItem() for i in rng]
                return listdelegators.ListDelegator(items)
            case _:
                raise TypeError(index)

    def __setitem__(self, index: int, value: widgets.QGraphicsItem):
        layoutitem = self.itemAt(index)
        layoutitem.setGraphicsItem(value)

    def __delitem__(self, index: int):
        self.removeAt(index)

    def __iter__(self) -> Iterator[widgets.QGraphicsItem]:
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item):
        return item in self.get_children()

    def __len__(self):
        # for PySide2
        return self.count()

    def get_children(self) -> listdelegators.ListDelegator[widgets.QGraphicsItem]:
        items = [self.itemAt(i).graphicsItem() for i in range(self.count())]
        return listdelegators.ListDelegator(items)

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)


class GraphicsLayout(GraphicsLayoutMixin, widgets.QGraphicsLayout):
    pass


if __name__ == "__main__":
    layout = GraphicsLayout()
