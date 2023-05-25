from __future__ import annotations

import enum
import logging

from prettyqt import constants, core, widgets
from prettyqt.utils import fuzzy
from prettyqt.qt import QtCore

logger = logging.getLogger(__name__)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_term = ""
        self.match_color: str | None = "blue"
        self.setSortRole(self.Roles.SortRole)
        self.sort(0, constants.DESCENDING)

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

    def lessThan(self, left, right):
        role = super().sortRole()
        left_data = left.data(role)
        right_data = right.data(role)
        if left_data is None or right_data is None:
            return True
        if self._search_term:
            return fuzzy.fuzzy_match(self._search_term, left_data) < fuzzy.fuzzy_match(
                self._search_term, right_data
            )
        else:
            return left_data < right_data

    def set_search_term(self, search_term: str):
        self._search_term = search_term
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
            case self.Roles.SortRole, _:
                idx = self.index(index.row(), filter_column)
                label = super().data(idx, constants.DISPLAY_ROLE)
                result = fuzzy.fuzzy_match(self._search_term, label)
                return result[1]
            case _, _:
                return super().data(index, role)


class FuzzyCompleter(widgets.Completer):
    def __init__(self, parent):
        super().__init__(parent)
        parent.setEditable(True)
        parent.set_insert_policy("no_insert")
        parent.installEventFilter(self)
        self.set_completion_mode("popup")
        self._local_completion_prefix = ""
        self._source_model = None
        self._filter_proxy = FuzzyFilterProxyModel(self)
        self._filter_proxy.set_match_color(None)
        self._using_original_model = False

    def setModel(self, model):
        self._source_model = model
        self._filter_proxy = FuzzyFilterProxyModel(self)
        self._filter_proxy.set_match_color(None)
        self._filter_proxy.setSourceModel(self._source_model)
        super().setModel(self._filter_proxy)
        self._using_original_model = True

    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent) -> bool:
        match event.type():
            case QtCore.QEvent.Type.FocusIn:
                source.clearEditText()
            case QtCore.QEvent.Type.KeyPress:
                key = event.key()
                if key == QtCore.Qt.Key.Key_Enter:
                    text = source.currentText()
                    source.setCompleter(None)
                    source.setEditText(text)
                    source.setCompleter(source.comp)
        return super().eventFilter(source, event)

    def updateModel(self):
        if not self._using_original_model:
            self._filter_proxy.setSourceModel(self._source_model)

        self._filter_proxy.set_search_term(self._local_completion_prefix)

    def splitPath(self, path):
        self._local_completion_prefix = path
        self.updateModel()
        if self._filter_proxy.rowCount() == 0:
            self._using_original_model = False
            self._filter_proxy.setSourceModel(core.StringListModel([path]))
            return [path]

        return []


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_models import JsonModel

    app = widgets.app()
    dist = [
        dict(
            assss=2,
            bffff={
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

    _source_model = JsonModel(dist)
    model = FuzzyFilterProxyModel()
    model.setFilterKeyColumn(1)
    cb = widgets.ComboBox()
    completer = FuzzyCompleter(cb)
    cb.setCompleter(completer)  #
    completer.set_strings(["Lola", "Lila", "Cola", "Lothian"])
    # cb.setModel(model)
    # cb.comp.setModel(model)
    # model.set_search_term("tj")
    model.setSourceModel(_source_model)
    widget = widgets.Widget()
    widget.set_layout("vertical")
    lineedit = widgets.LineEdit()
    lineedit.value_changed.connect(model.set_search_term)
    table = widgets.TreeView()
    table.set_delegate("html", column=1)
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)
    widget.box.add(cb)
    widget.box.add(lineedit)
    widget.box.add(table)
    widget.show()
    with app.debug_mode():
        app.main_loop()
