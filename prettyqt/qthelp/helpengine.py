from qtpy import QtHelp

from prettyqt import qthelp


QtHelp.QHelpEngine.__bases__ = (qthelp.HelpEngineCore,)


class HelpEngine(QtHelp.QHelpEngine):
    pass


if __name__ == "__main__":
    engine = HelpEngine("")
    engine.get_files("a", "b")
