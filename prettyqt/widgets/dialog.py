from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtWidgets


class DialogMixin(widgets.WidgetMixin):
    def __init__(
        self,
        *args,
        delete_on_close: bool = False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if delete_on_close:
            self.delete_on_close()

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
        return self.exec()


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
