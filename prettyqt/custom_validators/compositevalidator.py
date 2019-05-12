# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import gui


class CompositeValidator(gui.Validator):

    def __repr__(self):
        return f"CompositeValidator({self.validators})"

    def __init__(self, validators, parent=None):
        super().__init__(parent)
        self.validators = validators

    def __getstate__(self):
        return dict(validators=self.validators)

    def __setstate__(self, state):
        self.__init__(state["validators"])

    def validate(self, text, pos=0):
        vals = [v.validate(text, pos)[0] for v in self.validators]
        return (min(vals), text, pos)


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt import custom_validators
    val1 = custom_validators.NotEmptyValidator()
    val2 = custom_validators.PathValidator()
    val = CompositeValidator([val1, val2])
    app = widgets.Application.create_default_app()
    widget = widgets.LineEdit("This is a test")
    widget.setValidator(val)
    widget.show()
    app.exec_()
