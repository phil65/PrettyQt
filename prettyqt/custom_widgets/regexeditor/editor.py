"""
This module contains the editor widget implementation.
"""
import sre_constants
from prettyqt import widgets, core, custom_widgets, custom_models, constants
from prettyqt.syntaxhighlighters import RegexMatchHighlighter
try:
    import regex as re
except ImportError:
    import re


class RegexEditorWidget(widgets.Widget):
    quick_ref_requested = core.Signal(int)

    def __init__(self, title="Regex Editor", regex="", teststring="", parent=None):
        super().__init__(parent)
        self.resize(1200, 800)
        self.set_title(title)
        self.set_layout("horizontal")
        self.left_layout = widgets.BoxLayout("vertical")
        self.right_layout = widgets.BoxLayout("vertical")
        self.prog = None
        self.matches = None
        self.groupbox = widgets.GroupBox(title="Regular expression")
        self.grid = widgets.GridLayout(self.groupbox)
        self.label_error = widgets.Label("label_error")
        self.label_error.setStyleSheet("color: #FF0000;")
        self.grid.add(self.label_error, 2, 0)
        self.layout_toprow = widgets.BoxLayout("horizontal")
        self.lineedit_regex = widgets.LineEdit(regex)
        self.lineedit_regex.set_min_size(400, 0)
        self.layout_toprow.add(self.lineedit_regex)
        self.tb_flags = custom_widgets.BoolDictToolButton("Flags",
                                                          icon="mdi.flag-variant-outline")
        self.layout_toprow.add(self.tb_flags)
        self.grid.add(self.layout_toprow, 1, 0)
        self.left_layout.add(self.groupbox)
        self.groupbox_teststring = widgets.GroupBox(title="Test strings")
        self.layout_teststring = widgets.GridLayout(self.groupbox_teststring)
        self.textedit_teststring = widgets.PlainTextEdit(teststring)
        self.textedit_teststring.set_min_size(400, 0)
        self.layout_teststring.add(self.textedit_teststring, 0, 0)
        self.label_num_matches = widgets.Label("No match")
        self.label_num_matches.set_alignment("center")
        self.left_layout.add(self.groupbox_teststring)
        self.groupbox_substitution = widgets.GroupBox(title="Substitution",
                                                      checkable=True)
        self.layout_substitution = widgets.GridLayout(self.groupbox_substitution)
        self.lineedit_substitution = widgets.LineEdit()
        self.lineedit_substitution.textChanged.connect(self.update_sub_textedit)
        self.textedit_substitution = widgets.PlainTextEdit()
        self.textedit_substitution.set_min_size(400, 0)
        self.textedit_substitution.set_read_only()
        self.layout_substitution.add(self.lineedit_substitution, 0, 0)
        self.layout_substitution.add(self.textedit_substitution, 1, 0)
        self.left_layout.add(self.groupbox_substitution)
        self.cb_quickref = widgets.CheckBox("Show Regular Expression Quick Reference")
        self.left_layout.add(self.cb_quickref)
        self.table_matches = widgets.TableView()
        self.table_matches.setup_list_style()
        self.box.add(self.left_layout)
        self.box.add(self.right_layout)
        self.right_layout.add(self.label_num_matches)
        self.right_layout.add(self.table_matches)
        model = custom_models.RegexMatchesModel([])
        self.table_matches.setModel(model)
        self.table_matches.setColumnWidth(0, 60)
        self.table_matches.setColumnWidth(1, 60)
        self.groupbox_substitution.toggled.connect(self.lineedit_substitution.setVisible)
        self.groupbox_substitution.toggled.connect(self.textedit_substitution.setVisible)
        self.label_error.hide()
        self.lineedit_regex.textChanged.connect(self._update_view)
        doc = self.textedit_teststring.document()
        self._highlighter = RegexMatchHighlighter(doc)
        self._highlighter.rehighlight()
        self.cb_quickref.stateChanged.connect(self.quick_ref_requested)
        self.tb_flags.triggered.connect(self._update_view)
        self.textedit_teststring.textChanged.connect(self._update_view)
        dct = {"multiline": "MultiLine",
               "ignorecase": "Ignore case",
               "ascii": "ASCII-only matching",
               "dotall": "Dot matches newline",
               "verbose": "Ignore whitespace"}
        self._mapping = {"ignorecase": re.IGNORECASE,
                         "multiline": re.MULTILINE,
                         "ascii": re.ASCII,
                         "dotall": re.DOTALL,
                         "verbose": re.VERBOSE}
        self.tb_flags.set_dict(dct)
        self._update_view()

    @property
    def string(self):
        """
        Gets/Sets the test string
        """
        return self.textedit_teststring.text()

    @string.setter
    def string(self, value):
        self.textedit_teststring.set_text(value)

    @property
    def regex(self):
        """
        Gets/Sets the regular expression
        :return:
        """
        return self.lineedit_regex.text()

    @regex.setter
    def regex(self, value):
        self.lineedit_regex.set_text(value)

    @property
    def compile_flags(self):
        """
        Gets/Sets the compile flags
        :return:
        """
        ret_val = 0
        for identifier, flag in self._mapping.items():
            if self.tb_flags[identifier]:
                ret_val |= flag
        return ret_val

    @compile_flags.setter
    def compile_flags(self, value):
        for identifier, flag in self._mapping.items():
            self.tb_flags[identifier] = bool(value & flag)

    def on_match_list_current_change(self, index_new, index_old):
        model = self.table_matches.model()
        span = model.data(index_new, constants.USER_ROLE)
        self.textedit_teststring.select_text(*span)

    def _update_view(self):
        self.prog = None
        self.matches = None
        with self.textedit_teststring.block_signals():
            if not self.regex:
                self.label_error.hide()
                self._highlighter.set_spans(None)
                self.table_matches.setModel(None)
                self.label_num_matches.set_text("0 matches")
                return None
            try:
                self.prog = re.compile(self.regex, self.compile_flags)
            except sre_constants.error as e:
                self.label_error.show()
                self.label_error.set_text(f"Error: {e}")
                self._highlighter.set_spans(None)
                self.table_matches.setModel(None)
                self.label_num_matches.set_text("0 matches")
            except re._regex_core.error as e:
                self.label_error.show()
                self.label_error.set_text(f"Error: {e}")
                self._highlighter.set_spans(None)
                self.table_matches.setModel(None)
                self.label_num_matches.set_text("0 matches")
            else:
                self.label_error.hide()
                text = self.textedit_teststring.text()
                self.matches = list(self.prog.finditer(text))
                self.label_num_matches.set_text(f"{len(self.matches)} matches")
                model = custom_models.RegexMatchesModel(self.matches)
                self.table_matches.setModel(model)
                sel_model = self.table_matches.selectionModel()
                sel_model.currentChanged.connect(self.on_match_list_current_change)
                spans = [m.span() for m in self.matches]
                self._highlighter.set_spans(spans)
        self.update_sub_textedit()

    def update_sub_textedit(self):
        if self.prog:
            text = self.textedit_teststring.text()
            replace_with = self.lineedit_substitution.text()
            substituted = self.prog.sub(replace_with, text)
            self.textedit_substitution.set_text(substituted)
        else:
            self.textedit_substitution.set_text("")


if __name__ == "__main__":
    app = widgets.app()
    teststring = "aa356aa356aa356aa356aa356aa356aa356aa3a356aa356"
    widget = RegexEditorWidget(regex="aa[0-9]", teststring=teststring)
    widget.show()
    app.main_loop()
