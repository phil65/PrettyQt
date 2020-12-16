from typing import Iterator, List, Optional, Union

from qtpy import QtWidgets

from prettyqt import gui, widgets


QtWidgets.QToolBox.__bases__ = (widgets.Frame,)


class ToolBox(QtWidgets.QToolBox):
    def __getitem__(self, index: Union[int, str]) -> QtWidgets.QWidget:
        if isinstance(index, int):
            return self.widget(index)
        else:
            result = self.findChild(QtWidgets.QWidget, index)
            if result is None:
                raise KeyError("Widget not found")
            return result

    def __delitem__(self, index: int):
        self.removeItem(index)

    def serialize_fields(self):
        children = list()
        for i, widget in enumerate(self.get_children()):
            dct = dict(
                widget=widget,
                icon=gui.Icon(self.itemIcon(i)),
                text=self.itemText(i),
                enabled=self.isItemEnabled(i),
                tool_tip=self.itemToolTip(i),
            )
            children.append(dct)
        return dict(items=children, current_index=self.currentIndex())

    def __setstate__(self, state):
        for i, item in enumerate(state["items"]):
            self.addItem(item["widget"], item["icon"], item["text"])
            self.setItemEnabled(i, item["enabled"])
            self.setItemToolTip(i, item["tool_tip"])
        self.setCurrentIndex(state["current_index"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __iter__(self) -> Iterator[QtWidgets.QWidget]:
        return iter(self.get_children())

    def get_children(self) -> List[QtWidgets.QWidget]:
        return [self[i] for i in range(self.count())]

    def add_widget(
        self,
        widget: QtWidgets.QWidget,
        title: Optional[str] = None,
        icon: gui.icon.IconType = None,
    ):
        if title is None:
            title = widget.objectName()
        if icon:
            icon = gui.icon.get_icon(icon)
            self.addItem(widget, icon, title)
        else:
            self.addItem(widget, title)


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.Widget()
    w2 = widgets.Widget()
    tb = ToolBox()
    tb.add_widget(w, "title")
    tb.add_widget(w2)
    print(len(tb))
    tb.show()
    app.main_loop()
