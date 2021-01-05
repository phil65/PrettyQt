# see https://github.com/ITVRoC/SeekurJr/blob/master/seekur_12.04/packages/
# multimaster_fkie/node_manager_fkie/src/node_manager_fkie/yaml_highlighter.py


from __future__ import annotations

from prettyqt import core, gui, syntaxhighlighters


COMMENT_START = core.RegularExpression("#")
COMMENT_END = core.RegularExpression("\n|\r")  # Unused?
COMMENT_FORMAT = gui.TextCharFormat()
COMMENT_FORMAT.setFontItalic(True)
COMMENT_FORMAT.set_foreground_color("darkgray")


class Rule(syntaxhighlighters.HighlightRule):
    minimal = True


class Bool(Rule):
    regex = [r"\btrue\b", r"\bfalse\b"]
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
    RULES = Rule.__subclasses__()

    def highlightBlock(self, text: str):
        super().highlightBlock(text)
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = COMMENT_START.match(text).capturedStart()
            if start_index >= 0:
                comment_len = len(text) - start_index
                self.setFormat(start_index, comment_len, COMMENT_FORMAT)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = YamlHighlighter(editor.document())
    editor.show()
    app.main_loop()
