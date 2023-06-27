from __future__ import annotations

import enum
import logging

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import colors, datatypes, fuzzy
from prettyqt.qt import QtCore, QtGui

logger = logging.getLogger(__name__)


class FuzzyFilterProxyModel(core.SortFilterProxyModel):
    """Proxy model with fuzzyfilter functionality.

    this proxymodel replaces the text from the display role in the given filter column
    with HTML code in order to color the letter matches. A backup from the original text
    is made available in the BackupRole. Based on the original text, the proxy calculates
    a score for the match and makes it available via the SortRole.
    To display the html code properly, a HtmlItemDelegate is needed.

    """

    ID = "fuzzy"

    class Roles(enum.IntEnum):
        """Addional roles."""

        BackupRole = constants.USER_ROLE + 65
        SortRole = constants.SORT_ROLE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, filter_mode="fuzzy", **kwargs)
        self._search_term = ""
        self._match_color: QtGui.QColor = gui.Color("blue")
        self.sort(0, constants.DESCENDING)

    def set_match_color(self, color: datatypes.ColorType | None):
        self._match_color = colors.get_color(color) if color else QtGui.QColor()

    def get_match_color(self) -> QtGui.QColor:
        return self._match_color

    def lessThan(self, left: core.ModelIndex, right: core.ModelIndex):
        if not self._search_term:
            return super().lessThan(left, right)
        if left.data() is None or right.data() is None:
            return True
        # since fuzzy scores are cached, it should be fine to do this here.
        left_data = fuzzy.fuzzy_match(self._search_term, str(left.data()))
        right_data = fuzzy.fuzzy_match(self._search_term, str(right.data()))

        return left_data < right_data

    def set_search_term(self, search_term: str):
        self._search_term = search_term
        super().set_search_term(search_term)
        self.invalidate()

    def get_search_term(self):
        return self._search_term

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        filter_column = self.filterKeyColumn()
        match role, index.column():
            case constants.DISPLAY_ROLE, _ if index.column() == filter_column:
                label = super().data(index, constants.DISPLAY_ROLE)
                return (
                    fuzzy.color_text(
                        self._search_term,
                        str(label),
                        self._match_color.name(),
                        self.is_filter_case_sensitive(),
                    )
                    if self._search_term and self._match_color.isValid() and label
                    else label
                )
            # case constants.DISPLAY_ROLE, 1:
            #     idx = self.index(index.row(), filter_column)
            #     label = super().data(idx, constants.DISPLAY_ROLE)
            #     if label is None:
            #         return None
            #     result = fuzzy.fuzzy_match(self._search_term, str(label))
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

    search_term = core.Property(str, get_search_term, set_search_term)
    match_color = core.Property(QtGui.QColor, get_match_color, set_match_color)


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

    def eventFilter(self, source: widgets.QLineEdit, event: QtCore.QEvent) -> bool:
        match event.type():
            case QtCore.QEvent.Type.FocusIn:
                source.clearEditText()
            case QtCore.QEvent.Type.KeyPress:
                key = event.key()
                if key == constants.Key.Key_Enter:
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
            model = core.StringListModel([path])
            self._filter_proxy.setSourceModel(model)
            return [path]

        return []


if __name__ == "__main__":
    from prettyqt import custom_widgets
    import random
    import string

    app = widgets.app()
    window = widgets.MainWindow()
    pal = custom_widgets.CommandPalette()
    actions = [
        gui.Action(
            text="super duper action",
            shortcut="Ctrl+A",
            tool_tip="some Tooltip text",
            icon="mdi.folder",
            triggered=lambda: print("test"),
        ),
        gui.Action(
            text="this is an action",
            shortcut="Ctrl+B",
            tool_tip="Tooltip",
            icon="mdi.folder-outline",
            checked=True,
            checkable=True,
        ),
        gui.Action(
            text="another one P",
            shortcut="Ctrl+Alt+A",
            tool_tip="Some longer tooltiPpp",
            icon="mdi.folder",
        ),
        gui.Action(
            text="another onpe P",
            shortcut="Ctrl+Alt+A",
            tool_tip="Some longer tooltiPpp",
            icon="mdi.folder",
        ),
        gui.Action(text="a", shortcut="Ctrl+A", tool_tip="Tooltip", icon="mdi.folder"),
    ]
    pal.populate_from_widget(window)
    pal.add_actions(actions)
    for _ in range(500):
        label = "".join(random.choices(string.ascii_uppercase, k=10))
        pal.add_actions([gui.Action(text=label)])
    pal.show()
    with app.debug_mode():
        app.exec()
