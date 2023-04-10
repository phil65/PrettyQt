from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore


class RegexMatchesModel(core.AbstractTableModel):
    HEADER = ["Start", "End", "Value", "Groups"]

    def __init__(self, matches: list | None = None, parent: QtCore.QObject | None = None):
        super().__init__(parent=parent)
        self.matches = matches if matches else []

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def headerData(  # type: ignore
        self, section: int, orientation: QtCore.Qt.Orientation, role: int
    ) -> str | None:
        if role == constants.DISPLAY_ROLE:
            if orientation == constants.HORIZONTAL:
                return self.HEADER[section]

    def data(self, index, role):
        if not index.isValid():
            return None
        item = self.matches[index.row()]
        if role in [constants.DISPLAY_ROLE]:
            match index.column():
                case 0:
                    return str(item.span()[0])
                case 1:
                    return str(item.span()[1])
                case 2:
                    return repr(item.group())
                case 3:
                    return str(len(item.groups()))
        if role in [constants.USER_ROLE]:
            return item.span()

    def rowCount(self, parent=None):
        """Override for AbstractitemModel base method."""
        return len(self.matches)


if __name__ == "__main__":
    import re

    app = widgets.app()
    view = widgets.TableView()
    teststring = "fjdjkslfj355fjdkj 55 55454"
    regex = r"(?:[0-9])*.([0-9])"
    teststring = "SH_6208069141055_BC000388_20110412101855"
    regex = r"(?:([a-z]{2,})_)?(\d+)_([a-z]{2,}\d+)_(\d+)$"
    compiled = re.compile(regex, re.IGNORECASE)
    matches = list(compiled.finditer(teststring))
    model = RegexMatchesModel(matches)

    view.set_model(model)
    dlg = widgets.Dialog(layout="horizontal")
    dlg.add_widget(view)
    dlg.show_blocking()
    view.resize(500, 300)
    print(view.model())
    print(view.model().rowCount())
    app.main_loop()
