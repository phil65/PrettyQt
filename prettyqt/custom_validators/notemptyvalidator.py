from prettyqt import gui


class NotEmptyValidator(gui.Validator):
    def __eq__(self, other: object):
        return isinstance(other, NotEmptyValidator)

    def validate(self, text: str, pos: int = 0) -> tuple:
        if text == "":
            return (self.Intermediate, text, pos)
        return self.Acceptable, text, pos


if __name__ == "__main__":
    from prettyqt import widgets

    val = NotEmptyValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.main_loop()
