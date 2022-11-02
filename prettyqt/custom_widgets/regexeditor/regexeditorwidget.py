"""This module contains the editor widget implementation."""

from __future__ import annotations

from re import Match, Pattern
import sre_constants

import regex as re

from prettyqt import constants, core, custom_models, custom_widgets, widgets
from prettyqt.qt import QtWidgets
from prettyqt.syntaxhighlighters import RegexMatchHighlighter


class RegexEditorWidget(widgets.Widget):
    quick_ref_requested = core.Signal(int)

    def __init__(
        self,
        title: str = "Regex Editor",
        regex: str = "",
        teststring: str = "",
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        self.resize(1200, 800)
        self.set_title(title)
        self.set_icon("mdi.regex")
        self.set_layout("horizontal")
        self.left_layout = widgets.BoxLayout("vertical")
        self.right_layout = widgets.BoxLayout("vertical")
        self.prog: Pattern | None = None
        self.matches: list[Match] = list()
        self.groupbox = widgets.GroupBox(title="Regular expression")
        self.grid = widgets.GridLayout(self.groupbox)
        self.layout_toprow = widgets.BoxLayout("horizontal")
        self.regexinput = custom_widgets.RegexInput()
        self.regexinput.set_min_size(400, 0)
        self.layout_toprow.add(self.regexinput)
        self.grid.add(self.layout_toprow, 1, 0)
        self.left_layout.add(self.groupbox)
        self.groupbox_teststring = widgets.GroupBox(title="Test strings")
        self.groupbox_teststring.set_layout("grid")
        self.textedit_teststring = widgets.PlainTextEdit(teststring)
        self.textedit_teststring.set_min_size(400, 0)
        self.groupbox_teststring.box.add(self.textedit_teststring, 0, 0)
        self.label_num_matches = widgets.Label("No match")
        self.label_num_matches.set_alignment("center")
        self.left_layout.add(self.groupbox_teststring)
        self.groupbox_sub = widgets.GroupBox(title="Substitution", checkable=True)
        self.layout_sub = widgets.GridLayout(self.groupbox_sub)
        self.lineedit_sub = widgets.LineEdit()
        self.lineedit_sub.textChanged.connect(self.update_sub_textedit)
        self.textedit_sub = widgets.PlainTextEdit()
        self.textedit_sub.set_min_size(400, 0)
        self.textedit_sub.set_read_only()
        self.layout_sub.add(self.lineedit_sub, 0, 0)
        self.layout_sub.add(self.textedit_sub, 1, 0)
        self.left_layout.add(self.groupbox_sub)
        self.cb_quickref = widgets.CheckBox("Show Regular Expression Quick Reference")
        self.left_layout.add(self.cb_quickref)
        self.table_matches = widgets.TableView()
        self.table_matches.setup_list_style()
        self.box.add(self.left_layout)
        self.box.add(self.right_layout)
        self.right_layout.add(self.label_num_matches)
        self.right_layout.add(self.table_matches)
        model = custom_models.RegexMatchesModel()
        self.table_matches.set_model(model)
        self.table_matches.setColumnWidth(0, 60)
        self.table_matches.setColumnWidth(1, 60)
        self.groupbox_sub.toggled.connect(self.lineedit_sub.setVisible)
        self.groupbox_sub.toggled.connect(self.textedit_sub.setVisible)
        doc = self.textedit_teststring.document()
        self._highlighter = RegexMatchHighlighter(doc)
        self._highlighter.rehighlight()
        self.cb_quickref.stateChanged.connect(self.quick_ref_requested)
        self.regexinput.value_changed.connect(self._update_view)
        self.textedit_teststring.textChanged.connect(self._update_view)
        self.regexinput.pattern = regex
        self._update_view()

    def __getattr__(self, attr):
        return self.regexinput.__getattribute__(attr)

    def on_match_list_current_change(self, index_new, index_old):
        model = self.table_matches.model()
        span = model.data(index_new, constants.USER_ROLE)  # type: ignore
        self.textedit_teststring.select_text(*span)

    def _update_view(self) -> None:
        self.prog = None
        self.matches = list()
        with self.textedit_teststring.block_signals():
            if not self.pattern:
                self._highlighter.set_spans(None)
                self.table_matches.set_model(None)
                self.label_num_matches.set_text("0 matches")
                return None
            try:
                self.prog = re.compile(self.pattern, self.compile_flags)
            except sre_constants.error:
                self._highlighter.set_spans(None)
                self.table_matches.set_model(None)
                self.label_num_matches.set_text("0 matches")
            except re._regex_core.error:
                self._highlighter.set_spans(None)
                self.table_matches.set_model(None)
                self.label_num_matches.set_text("0 matches")
            else:
                text = self.textedit_teststring.text()
                self.matches = list(self.prog.finditer(text))
                self.label_num_matches.set_text(f"{len(self.matches)} matches")
                model = custom_models.RegexMatchesModel(self.matches)
                self.table_matches.set_model(model)
                sel_model = self.table_matches.selectionModel()
                sel_model.currentChanged.connect(self.on_match_list_current_change)
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
    app.setApplicationName("Test")
    app.setOrganizationName("Test")
    teststring = "aa356aa356aa356aa356aa356aa356aa356aa3a356aa356"
    widget = RegexEditorWidget(regex="aa[0-9]", teststring=teststring)
    widget.show()
    app.main_loop()
