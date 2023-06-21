from __future__ import annotations

from collections.abc import Iterator

from prettyqt import gui, iconprovider, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import datatypes, listdelegators


class ToolBox(widgets.FrameMixin, QtWidgets.QToolBox):
    def __getitem__(
        self, index: int | str
    ) -> QtWidgets.QWidget | listdelegators.BaseListDelegator[QtWidgets.QWidget]:
        match index:
            case int():
                return self.widget(index)
            case str():
                result = self.find_child(QtWidgets.QWidget, index)
                if result is None:
                    raise KeyError("Widget not found")
                return result
            case slice():
                stop = index.stop or self.count()
                rng = range(index.start or 0, stop, index.step or 1)
                widgets = [self.widget(i) for i in rng]
                return listdelegators.BaseListDelegator(widgets)
            case _:
                raise TypeError(index)

    def __delitem__(self, index: int):
        self.removeItem(index)

    # def __setstate__(self, state):
    #     for i, item in enumerate(state["items"]):
    #         self.addItem(item["widget"], item["icon"], item["text"])
    #         self.setItemEnabled(i, item["enabled"])
    #         self.setItemToolTip(i, item["tool_tip"])
    #     self.setCurrentIndex(state["current_index"])

    # def __reduce__(self):
    #     return type(self), (), self.__getstate__()

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.get_children())

    def __contains__(self, item: QtWidgets.QWidget):
        return self.indexOf(item) >= 0

    def get_children(self) -> listdelegators.BaseListDelegator[QtWidgets.QWidget]:
        widgets = [self.widget(i) for i in range(self.count())]
        return listdelegators.BaseListDelegator(widgets)

    def add_widget(
        self,
        widget: QtWidgets.QWidget,
        title: str | None = None,
        icon: datatypes.IconType = None,
        tooltip: str = "",
        enabled: bool = True,
    ):
        title = widget.objectName() if title is None else title
        icon = iconprovider.get_icon(icon) if icon else gui.Icon()
        self.addItem(widget, icon, title)
        index = self.indexOf(widget)
        if tooltip:
            self.setItemToolTip(index, tooltip)
        self.setItemEnabled(index, enabled)

    def get_item_icon(self, index: int) -> gui.Icon | None:
        icon = self.itemIcon(index)
        return None if icon.isNull() else gui.Icon(icon)


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Widget()
    w2 = widgets.Widget()
    tb = ToolBox()
    tb.add_widget(w, "title")
    tb.add_widget(w2)
    tb.show()
    app.exec()
