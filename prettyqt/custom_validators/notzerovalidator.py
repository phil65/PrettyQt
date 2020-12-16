from prettyqt import gui


class NotZeroValidator(gui.Validator):
    def validate(self, text: str, pos: int = 0) -> tuple:
        if text == "0":
            return self.Intermediate, text, pos
        return self.Acceptable, text, pos

    def __eq__(self, other: object):
        return isinstance(other, NotZeroValidator)


if __name__ == "__main__":
    from prettyqt import widgets

    val = NotZeroValidator()
    app = widgets.app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.main_loop()
