"""
This module contains the editor widget implementation.
"""
import re
import sre_constants
from prettyqt import widgets, core, custom_widgets
from prettyqt.custom_widgets.regexeditor import match_highlighter


class RegexEditorWidget(widgets.Widget):
    quick_ref_requested = core.Signal(int)

    def __init__(self, title="Regex Editor", parent=None):
        super().__init__(parent)
        self.resize(537, 377)
        self.set_title(title)
        self.set_layout("vertical")
        self.prog = None
        self.groupbox = widgets.GroupBox(title="Regular expression")
        self.grid = widgets.GridLayout(self.groupbox)
        self.label_error = widgets.Label("label_error")
        self.label_error.setStyleSheet("color: #FF0000;")
        self.grid.add(self.label_error, 2, 0)
        self.layout_toprow = widgets.BoxLayout("horizontal")
        self.lineedit_regex = widgets.LineEdit()
        self.lineedit_regex.set_min_size(400, 0)
        self.layout_toprow.add(self.lineedit_regex)
        self.tb_flags = custom_widgets.BoolDictToolButton("Flags",
                                                          icon="mdi.flag-variant-outline")
        self.layout_toprow.add(self.tb_flags)
        self.grid.add(self.layout_toprow, 1, 0)
        self.box.add(self.groupbox)
        self.groupbox_teststring = widgets.GroupBox(title="Test strings")
        self.layout_teststring = widgets.GridLayout(self.groupbox_teststring)
        self.textedit_teststring = widgets.PlainTextEdit()
        self.textedit_teststring.set_min_size(400, 0)
        self.layout_teststring.add(self.textedit_teststring, 0, 0)
        self.box.add(self.groupbox_teststring)
        self.groupbox_substitution = widgets.GroupBox(title="Substitution",
                                                      checkable=True)
        self.layout_substitution = widgets.GridLayout(self.groupbox_substitution)
        self.lineedit_substitution = widgets.LineEdit()
        self.lineedit_substitution.textChanged.connect(self.update_sub_textedit)
        self.textedit_substitution = widgets.PlainTextEdit()
        self.groupbox_substitution.toggled.connect(self.lineedit_substitution.setVisible)
        self.groupbox_substitution.toggled.connect(self.textedit_substitution.setVisible)
        self.textedit_substitution.set_min_size(400, 0)
        self.textedit_substitution.set_read_only()
        self.layout_substitution.add(self.lineedit_substitution, 0, 0)
        self.layout_substitution.add(self.textedit_substitution, 1, 0)
        self.box.add(self.groupbox_substitution)
        self.cb_quickref = widgets.CheckBox("Show Regular Expression Quick Reference")
        self.box.add(self.cb_quickref)
        self.label_error.hide()
        self.lineedit_regex.textChanged.connect(self._update_view)
        doc = self.textedit_teststring.document()
        self._highlighter = match_highlighter.MatchHighlighter(doc)
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

    def _update_view(self, *args):
        with self.textedit_teststring.block_signals():
            if not self.regex:
                self.label_error.hide()
                self._highlighter.set_prog(None)
                return None
            try:
                self.prog = re.compile(self.regex, self.compile_flags)
            except sre_constants.error as e:
                self.prog = None
                self.label_error.show()
                self.label_error.set_text('Error: %s' % e)
                self._highlighter.set_prog(None)
            else:
                self.label_error.hide()
                self._highlighter.set_prog(self.prog)
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
    widget = RegexEditorWidget()
    widget.show()
    app.main_loop()
