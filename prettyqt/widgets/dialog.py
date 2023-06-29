from __future__ import annotations

from prettyqt import constants, widgets


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
            case constants.Key.Key_Escape:
                self.close()
            case constants.Key.Key_F11 if self.isMaximized():
                self.showNormal()
            case constants.Key.Key_F11:
                self.showMaximized()
            case _:
                super().keyPressEvent(e)

    def delete_on_close(self):
        self.setAttribute(constants.WidgetAttribute.WA_DeleteOnClose)

    def add_buttonbox(self) -> widgets.DialogButtonBox:
        button_box = widgets.DialogButtonBox.create(ok=self.accept, cancel=self.reject)
        self.box.add(button_box)
        return button_box

    def show_blocking(self) -> bool:
        self.show()
        return bool(self.exec())

    def is_accepted(self) -> bool:
        return self.result() == widgets.QDialog.DialogCode.Accepted

    def main_loop(self) -> int:
        return self.exec()


class Dialog(DialogMixin, widgets.QDialog):
    pass


if __name__ == "__main__":
    import pathlib
    import pickle

    app = widgets.app()
    w = Dialog()
    path = pathlib.Path("data.pkl")
    with path.open("wb") as writer:
        pickle.dump(w, writer)
    with path.open("rb") as reader:
        w = pickle.load(reader)
    w.show_blocking()
