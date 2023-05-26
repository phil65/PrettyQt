from __future__ import annotations

from prettyqt import qthelp
from prettyqt.qt import QtHelp


class HelpEngine(qthelp.HelpEngineCoreMixin, QtHelp.QHelpEngine):
    def get_content_model(self) -> qthelp.HelpContentModel:
        return qthelp.HelpContentModel(self.contentModel())


if __name__ == "__main__":
    engine = HelpEngine("")
    engine.get_files("a", "b")
