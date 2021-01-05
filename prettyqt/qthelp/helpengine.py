from __future__ import annotations

from prettyqt import qthelp
from prettyqt.qt import QtHelp


QtHelp.QHelpEngine.__bases__ = (qthelp.HelpEngineCore,)


class HelpEngine(QtHelp.QHelpEngine):
    pass


if __name__ == "__main__":
    engine = HelpEngine("")
    engine.get_files("a", "b")
