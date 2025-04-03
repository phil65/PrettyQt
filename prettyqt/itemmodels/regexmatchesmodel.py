from __future__ import annotations

import re
from typing import ClassVar

from prettyqt import constants, core


class RegexMatchesModel(core.AbstractTableModel):
    """Model to display a list of re.Matches."""

    HEADER: ClassVar = ["Start", "End", "Value", "Groups"]
    SUPPORTS = list[re.Match]

    def __init__(self, matches: list | None = None, **kwargs):
        super().__init__(**kwargs)
        self.matches = matches or []

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (re.Match(), *_):
                return True
            case _:
                return False

    def columnCount(self, parent=None):
        return len(self.HEADER)

    def headerData(  # type: ignore
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.HEADER[section]

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        item = self.matches[index.row()]
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return str(item.span()[0])
            case constants.DISPLAY_ROLE, 1:
                return str(item.span()[1])
            case constants.DISPLAY_ROLE, 2:
                return repr(item.group())
            case constants.DISPLAY_ROLE, 3:
                return str(len(item.groups()))
            case constants.USER_ROLE, _:
                return item.span()

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self.matches)


if __name__ == "__main__":
    from prettyqt import widgets

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
    dlg = widgets.Dialog()
    dlg.set_layout("horizontal")
    dlg.box.add_widget(view)
    dlg.show_blocking()
    view.resize(500, 300)
    app.exec()
