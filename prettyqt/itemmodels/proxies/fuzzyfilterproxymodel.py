from __future__ import annotations

import enum
import logging
from typing import TYPE_CHECKING

import sublime_search

from prettyqt import constants, core, gui
from prettyqt.utils import colors, fuzzy


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class FuzzyFilterProxyModel(core.SortFilterProxyModel):
    """A FilterProxyModel which sorts the results based on a matching score.

    The matching score evaluates metrics like upper/lower casing, distance of
    filter character to match character and some more.
    Best matches are shown at the top.

    The matching score is exposed as a custom UserRole
    (FuzzyFilterProxyModel.Roles.SortRole)
    The proxymodel replaces the text from the display role in the given filter column
    with HTML code in order to color the letter matches. A backup from the original text
    is made available in the BackupRole. Based on the original text, the proxy calculates
    a score for the match and makes it available via the SortRole.
    To display the html code properly, a HtmlItemDelegate is needed.

    ### Example

    ```py
    proxy = itemmodels.FuzzyFilterProxyModel()
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "fuzzy"

    class Roles(enum.IntEnum):
        """Addional roles."""

        BackupRole = constants.USER_ROLE + 65
        SortRole = constants.SORT_ROLE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, filter_mode="fuzzy", **kwargs)
        self._search_term = ""
        self._match_color: gui.QColor = gui.Color("blue")
        self.sort(0, constants.DESCENDING)

    def set_match_color(self, color: datatypes.ColorType | None):
        self._match_color = colors.get_color(color) if color else gui.QColor()

    def get_match_color(self) -> gui.QColor:
        return self._match_color

    def lessThan(self, left: core.ModelIndex, right: core.ModelIndex):
        if not self._search_term:
            return super().lessThan(left, right)
        if left.data() is None or right.data() is None:
            return True
        # since fuzzy scores are cached, it should be fine to do this here.
        left_data = sublime_search.fuzzy_match(self._search_term, str(left.data()))
        right_data = sublime_search.fuzzy_match(self._search_term, str(right.data()))

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
            #     result = sublime_search.fuzzy_match(self._search_term, str(label))
            #     return str(result[1])
            case self.Roles.BackupRole, _:
                return super().data(index, constants.DISPLAY_ROLE)
            case self.Roles.SortRole, _:
                idx = self.index(index.row(), filter_column)
                label = super().data(idx, constants.DISPLAY_ROLE)
                result = sublime_search.fuzzy_match(self._search_term, label)
                return result[1]
            case _, _:
                return super().data(index, role)

    search_term = core.Property(
        str,
        get_search_term,
        set_search_term,
        doc="Current search term",
    )
    match_color = core.Property(
        gui.QColor,
        get_match_color,
        set_match_color,
        doc="Color to use for match coloring",
    )


if __name__ == "__main__":
    import random
    import string

    from prettyqt import custom_widgets, widgets

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
