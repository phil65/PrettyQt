# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""
# see https://github.com/ITVRoC/SeekurJr/blob/master/seekur_12.04/packages/
# multimaster_fkie/node_manager_fkie/src/node_manager_fkie/yaml_highlighter.py


from prettyqt import core, gui, syntaxhighlighters

COMMENT_START = core.RegExp("#")
COMMENT_END = core.RegExp("\n|\r")  # Unused?
COMMENT_FORMAT = gui.TextCharFormat()
COMMENT_FORMAT.setFontItalic(True)
COMMENT_FORMAT.set_foreground_color("darkgray")


class Rule(syntaxhighlighters.HighlightRule):
    minimal = True


class Bool(Rule):
    regex = ["\\btrue\\b", "\\bfalse\\b"]
    color = "blue"
    bold = True


class Decimal(Rule):
    regex = r"\d+"
    color = "darkMagenta"


class Rule2(Rule):
    regex = r"^\s*[_.\w]*\s*:"
    color = "blue"


class Rule3(Rule):
    regex = r":\s*:[_\.\w]*$|:\s*\@[_\.\w]*$"
    color = "blue"


class ListMember(Rule):
    regex = r"^\s*-"
    color = "red"
    bold = True


class DocumentStart(Rule):
    regex = r"^---$"
    color = "red"
    bold = True


class Brackets(Rule):
    regex = r"[\[\]\{\}\,]"
    color = "darkgreen"
    bold = True


class Rule7(Rule):
    regex = r"\".*\"|\'.*\'"
    color = "darkorange"


class Rule8(Rule):
    regex = r"\$\(.*\)"
    color = "orange"


class DocType(Rule):
    regex = r"<!DOCTYPE.*>"
    color = "lightgray"


class Xml(Rule):
    regex = r"<\?xml.*\?>"
    color = "lightgray"


class YamlHighlighter(gui.SyntaxHighlighter):
    """
    Enabled the syntax highlightning for the yaml files.
    """

    def highlightBlock(self, text):
        for pattern, form in Rule.yield_rules():
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, form)
                index = pattern.indexIn(text, index + length)
    # mark comment blocks
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = COMMENT_START.indexIn(text)
            if start_index >= 0:
                comment_len = len(text) - start_index
                self.setFormat(start_index, comment_len, COMMENT_FORMAT)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = YamlHighlighter(editor.document())
    editor.show()
    app.exec_()
