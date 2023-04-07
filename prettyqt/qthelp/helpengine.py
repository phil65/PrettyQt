from __future__ import annotations

from prettyqt import qthelp
from prettyqt.qt import QtHelp


class HelpEngine(qthelp.HelpEngineCoreMixin, QtHelp.QHelpEngine):
    pass


if __name__ == "__main__":
    engine = HelpEngine("")
    engine.get_files("a", "b")
