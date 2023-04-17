from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import datatypes


class DialogMixin(widgets.WidgetMixin):
    def __init__(
        self,
        title: str = "",
        icon: datatypes.IconType = None,
        parent: QtWidgets.QWidget | None = None,
        delete_on_close: bool = False,
        layout: None | str | QtWidgets.QLayout = None,
    ):
        super().__init__(parent=parent)
        self.set_title(title)
        self.set_icon(icon)
        if delete_on_close:
            self.delete_on_close()
        if layout is not None:
            self.set_layout(layout)

    def __getitem__(self, index: str) -> QtWidgets.QWidget:
        result = self.find_child(QtWidgets.QWidget, index)
        if result is None:
            raise KeyError("Widget not found")
        return result

    def serialize_fields(self):
        return dict(
            # modal=self.isModal(),
            layout=self.layout(),
            size_grip_enabled=self.isSizeGripEnabled(),
            size=(self.size().width(), self.size().height()),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        if state["layout"]:
            self.set_layout(state["layout"])
        self.resize(*state["size"])
        self.setSizeGripEnabled(state["size_grip_enabled"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def keyPressEvent(self, e):
        match e.key():
            case QtCore.Qt.Key.Key_Escape:
                self.close()
            case QtCore.Qt.Key.Key_F11 if self.isMaximized():
                self.showNormal()
            case QtCore.Qt.Key.Key_F11:
                self.showMaximized()
            case _:
                super().keyPressEvent(e)

    def delete_on_close(self):
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

    def add_widget(self, widget: QtWidgets.QWidget) -> QtWidgets.QWidget:
        self.box += widget
        return widget

    def add_buttonbox(self) -> widgets.DialogButtonBox:
        button_box = widgets.DialogButtonBox.create(ok=self.accept, cancel=self.reject)
        self.box.add(button_box)
        return button_box

    def show_blocking(self) -> bool:
        self.show()
        return bool(self.main_loop())

    def is_accepted(self) -> bool:
        return self.result() == QtWidgets.QDialog.DialogCode.Accepted

    def main_loop(self) -> int:
        return self.exec_()


class Dialog(DialogMixin, QtWidgets.QDialog):
    pass


if __name__ == "__main__":
    app = widgets.app()
    w = Dialog()
    import pickle

    with open("data.pkl", "wb") as writer:
        pickle.dump(w, writer)
    with open("data.pkl", "rb") as reader:
        w = pickle.load(reader)
    w.show_blocking()
