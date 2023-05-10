from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import fuzzy


def bold(text: str) -> str:
    return f"<b>{text}</b>"


def colored(text: str, color: str) -> str:
    return f"<font color={color!r}>{text}</font>"


def color_text(input_text: str, text: str, color: str, case_sensitive: bool = False):
    def converter(x):
        return x if case_sensitive else x.lower()

    output_text = ""
    for char in text:
        if input_text and converter(char) == converter(input_text[0]):
            output_text += bold(colored(char, color))
            input_text = input_text[1:]
        else:
            output_text += char
    return output_text


class FuzzyFilterModelMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_marker_text = ""
        self.filter_column = 0
        self.match_color = "blue"
        self.case_sensitive = False

    def set_current_marker_text(self, text: str):
        with self.reset_model():
            self.current_marker_text = text

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        match role, index.column():
            case constants.DISPLAY_ROLE, self.filter_column:
                label = super().data(index, role)
                return (
                    color_text(
                        self.current_marker_text,
                        label,
                        self.match_color,
                        self.case_sensitive,
                    )
                    if self.current_marker_text
                    else label
                )
            # case constants.DISPLAY_ROLE, 1:
            #     idx = self.index(index.row(), self.filter_column)
            #     label = super().data(idx, constants.DISPLAY_ROLE)
            #     result = fuzzy.fuzzy_match(self.current_marker_text, label)
            #     return str(result[1])
            case constants.SORT_ROLE, _:
                idx = self.index(index.row(), self.filter_column)
                label = super().data(idx, constants.DISPLAY_ROLE)
                result = fuzzy.fuzzy_match(self.current_marker_text, label)
                return result[1]
            case _, _:
                return super().data(index, role)


class FuzzyFilterProxyModel(core.SortFilterProxyModel):
    def __init__(self, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._search_term = ""

    def filterAcceptsRow(self, source_row: int, source_index: core.ModelIndex):
        column = self.filterKeyColumn()
        idx = self.sourceModel().index(source_row, column, source_index)
        text = self.sourceModel().data(idx)
        if self._search_term == "":
            return True
        return fuzzy.fuzzy_match_simple(
            self._search_term, text, case_sensitive=self.is_filter_case_sensitive()
        )

    def set_search_term(self, search_term: str):
        self._search_term = search_term
        self.invalidate()
        self.sort(0, constants.DESCENDING)


if __name__ == "__main__":
    from prettyqt import custom_delegates, widgets
    from prettyqt.custom_models import JsonModel

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

    class Model(FuzzyFilterModelMixin, JsonModel):
        pass

    source_model = Model(dist)
    source_model.filter_column = 1
    model = FuzzyFilterProxyModel()
    model.setFilterKeyColumn(1)
    # model.set_search_term("tj")
    model.setSourceModel(source_model)
    widget = widgets.Widget()
    widget.set_layout("vertical")
    lineedit = widgets.LineEdit()
    lineedit.value_changed.connect(model.set_search_term)
    lineedit.value_changed.connect(source_model.set_current_marker_text)
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
