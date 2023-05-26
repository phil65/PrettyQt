from __future__ import annotations

from prettyqt import qthelp
from prettyqt.qt import QtHelp


class HelpEngine(qthelp.HelpEngineCoreMixin, QtHelp.QHelpEngine):
    def get_content_model(self) -> qthelp.HelpContentModel:
        model = self.contentModel()
        model.__class__ = qthelp.HelpContentModel
        return model


if __name__ == "__main__":
    engine = HelpEngine("")
    model = engine.get_content_model()
    print(model)
    engine.get_files("a", "b")
