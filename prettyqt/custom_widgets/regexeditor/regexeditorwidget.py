"""This module contains the editor widget implementation."""

from __future__ import annotations

import pathlib
import re
import re._constants as sre_constants  # pyright: ignore
from typing import TYPE_CHECKING

from prettyqt import constants, core, custom_widgets, itemmodels, widgets
from prettyqt.syntaxhighlighters import RegexMatchHighlighter


if TYPE_CHECKING:
    from re import Match, Pattern


REF_HTML_FILE = pathlib.Path(__file__).parent / "ref.html"
URL = "https://jex.im/regulex/#!embed=true&flags=&re={ESCAPED_REGEX}"


class RegexEditorWidget(widgets.Widget):
    quick_ref_requested = core.Signal(int)

    def __init__(
        self,
        title: str = "Regex Editor",
        regex: str = "",
        teststring: str = "",
        parent: widgets.QWidget | None = None,
    ):
        super().__init__(window_icon="mdi.regex", window_title=title, parent=parent)
        self.resize(1200, 800)
        self.prog: Pattern | None = None
        self.matches: list[Match] = []
        self.textedit_teststring = widgets.PlainTextEdit(teststring, minimum_width=400)
        self.regexinput = custom_widgets.RegexInput(minimum_width=400)
        self.label_num_matches = widgets.Label("No match", alignment="center")
        self.lineedit_sub = widgets.LineEdit(text_changed=self.update_sub_textedit)
        self.textedit_sub = widgets.PlainTextEdit(read_only=True, minimum_width=400)
        self.table_matches = widgets.TableView()
        self.table_matches.setup_list_style()
        textedit_quickref = widgets.TextEdit(
            parent=self,
            read_only=True,
            object_name="textedit_quickref",
            html=REF_HTML_FILE.read_text("utf-8"),
        )
        cb_quickref = widgets.CheckBox(
            "Show Regular Expression Quick Reference",
            checked=True,
            state_changed=textedit_quickref.setVisible,
        )
        model = itemmodels.RegexMatchesModel()
        self.table_matches.set_model(model)
        self.table_matches.setColumnWidth(0, 60)
        self.table_matches.setColumnWidth(1, 60)
        doc = self.textedit_teststring.document()
        self._highlighter = RegexMatchHighlighter(doc)
        self._highlighter.rehighlight()
        self.regexinput.value_changed.connect(self._update_view)
        self.textedit_teststring.textChanged.connect(self._update_view)
        self.regexinput.pattern = regex  # pyright: ignore
        groupbox = widgets.GroupBox(title="Regular expression")
        layout_toprow = widgets.HBoxLayout()
        layout_toprow.add(self.regexinput)
        grid = widgets.GridLayout(groupbox)
        grid[1, 0] = layout_toprow
        groupbox_teststring = widgets.GroupBox(title="Test strings")
        groupbox_teststring.set_layout("grid")
        groupbox_teststring.box[0, 0] = self.textedit_teststring
        groupbox_sub = widgets.GroupBox(title="Substitution", checkable=True)
        groupbox_sub.toggled.connect(self.lineedit_sub.setVisible)
        groupbox_sub.toggled.connect(self.textedit_sub.setVisible)
        layout_sub = widgets.GridLayout(groupbox_sub)
        layout_sub[0, 0] = self.lineedit_sub
        layout_sub[1, 0] = self.textedit_sub
        layout = self.set_layout("horizontal")
        with layout.get_sub_layout("vertical") as layout:
            layout.add(groupbox)
            layout.add(groupbox_teststring)
            layout.add(groupbox_sub)
            layout.add(cb_quickref)
        sub_layout = widgets.VBoxLayout()
        layout.add(sub_layout)
        sub_layout.add(self.label_num_matches)
        # TODO: adding table to layout weirdly breaks tests
        sub_layout.add(self.table_matches)
        layout.add(textedit_quickref)
        self._update_view()

    def on_match_list_current_change(self, index_new, index_old):
        model = self.table_matches.model()
        span = model.data(index_new, constants.USER_ROLE)  # type: ignore
        self.textedit_teststring.selecter.select_text(*span)

    def _update_view(self):
        self.prog = None
        self.matches = []
        with self.textedit_teststring.signals_blocked():
            if not self.regexinput.get_pattern():
                self._highlighter.set_spans(None)
                self.table_matches.set_model(None)
                self.label_num_matches.set_text("0 matches")
                return
            try:
                self.prog = re.compile(
                    self.regexinput.get_pattern(), self.regexinput.get_flags()
                )
            except sre_constants.error:
                self._highlighter.set_spans(None)
                self.table_matches.set_model(None)
                self.label_num_matches.set_text("0 matches")
            else:
                text = self.textedit_teststring.text()
                self.matches = list(self.prog.finditer(text))
                self.label_num_matches.set_text(f"{len(self.matches)} matches")
                model = itemmodels.RegexMatchesModel(self.matches)
                self.table_matches.set_model(model)
                sel_model = self.table_matches.selectionModel()
                sel_model.currentRowChanged.connect(self.on_match_list_current_change)
                spans = [m.span() for m in self.matches]
                self._highlighter.set_spans(spans)
        self.update_sub_textedit()

    def update_sub_textedit(self):
        if self.prog:
            text = self.textedit_teststring.text()
            replace_with = self.lineedit_sub.text()
            substituted = self.prog.sub(replace_with, text)
            self.textedit_sub.set_text(substituted)
        else:
            self.textedit_sub.set_text("")


if __name__ == "__main__":
    app = widgets.app()
    teststring = "aa356aa356aa356aa356aa356aa356aa356aa3a356aa356"
    widget = RegexEditorWidget(regex="aa[0-9]", teststring=teststring)
    widget.show()
    app.exec()
