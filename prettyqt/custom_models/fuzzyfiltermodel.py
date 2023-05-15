from __future__ import annotations

import enum
import logging

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import fuzzy


logger = logging.getLogger(__name__)


class FuzzyFilterSortScoreModel(core.IdentityProxyModel):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._search_term = ""

    class Roles(enum.IntEnum):
        """Addional roles."""

        SortRole = constants.SORT_ROLE

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        match role:
            case self.Roles.SortRole:
                label = super().data(index, constants.DISPLAY_ROLE)
                result = fuzzy.fuzzy_match(self._search_term, label)
                return result[1]
            case _:
                return super().data(index, role)


class FuzzyFilterProxyModel(core.SortFilterProxyModel):
    """Proxy model with fuzzyfilter functionality.

    this proxymodel replaces the text from the display role in the given filter column
    with HTML code in order to color the letter matches. A backup from the original text
    is made available in the BackupRole. Based on the original text, the proxy calculates
    a score for the match and makes it available via the SortRole.
    To display the html code properly, a HtmlItemDelegate is needed.

    """

    class Roles(enum.IntEnum):
        """Addional roles."""

        BackupRole = constants.USER_ROLE + 65
        SortRole = constants.SORT_ROLE

    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._search_term = ""
        self.match_color: str | None = "blue"
        self.setSortRole(self.Roles.SortRole)
        self.sort(0, constants.DESCENDING)

    def setSourceModel(self, model):
        self._proxy = FuzzyFilterSortScoreModel()
        super().setSourceModel(self._proxy)
        self._proxy.setSourceModel(model)

    def set_match_color(self, color):
        self.match_color = color

    def filterAcceptsRow(self, source_row: int, source_index: core.ModelIndex) -> bool:
        if self._search_term == "":
            return True
        column = self.filterKeyColumn()
        source_model = self.sourceModel()
        idx = source_model.index(source_row, column, source_index)
        text = source_model.data(idx)
        return fuzzy.fuzzy_match_simple(
            self._search_term, text, case_sensitive=self.is_filter_case_sensitive()
        )

    def set_search_term(self, search_term: str):
        self._search_term = search_term
        self._proxy._search_term = search_term
        self.invalidate()

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        filter_column = self.filterKeyColumn()
        match role, index.column():
            case constants.DISPLAY_ROLE, _ if index.column() == filter_column:
                label = super().data(index, constants.DISPLAY_ROLE)
                # logging.info(label)
                return (
                    fuzzy.color_text(
                        self._search_term,
                        str(label),
                        self.match_color,
                        self.is_filter_case_sensitive(),
                    )
                    if self._search_term and self.match_color
                    else label
                )
            # case constants.DISPLAY_ROLE, 1:
            #     idx = self.index(index.row(), filter_column)
            #     label = super().data(idx, constants.DISPLAY_ROLE)
            #     result = fuzzy.fuzzy_match(self._search_term, label)
            #     return str(result[1])
            case self.Roles.BackupRole, _:
                return super().data(index, constants.DISPLAY_ROLE)
            case _, _:
                return super().data(index, role)


if __name__ == "__main__":
    import sys

    from prettyqt import custom_delegates, widgets
    from prettyqt.custom_models import JsonModel

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    app = widgets.app()
    dist = [
        dict(
            a=2,
            b={
                "a": 4,
                "b": [1, 2, 3],
                "jkjkjk": "tekjk",
                "sggg": "tekjk",
                "fdfdf": "tekjk",
                "xxxx": "xxx",
            },
        ),
        6,
        "jkjk",
    ]

    source_model = JsonModel(dist)
    model = FuzzyFilterProxyModel()
    model.setFilterKeyColumn(1)
    # model.set_search_term("tj")
    model.setSourceModel(source_model)
    widget = widgets.Widget()
    widget.set_layout("vertical")
    lineedit = widgets.LineEdit()
    lineedit.value_changed.connect(model.set_search_term)
    delegate = custom_delegates.HtmlItemDelegate()
    table = widgets.TreeView()
    table.setItemDelegateForColumn(1, delegate)
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)
    widget.box.add(lineedit)
    widget.box.add(table)
    widget.show()
    app.main_loop()
