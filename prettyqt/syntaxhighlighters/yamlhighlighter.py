# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""
# see https://github.com/ITVRoC/SeekurJr/blob/master/seekur_12.04/packages/
# multimaster_fkie/node_manager_fkie/src/node_manager_fkie/yaml_highlighter.py


from prettyqt import core, gui

COMMENT_START = core.RegExp("#")
COMMENT_END = core.RegExp("\n|\r")  # Unused?
COMMENT_FORMAT = gui.TextCharFormat()
COMMENT_FORMAT.setFontItalic(True)
COMMENT_FORMAT.set_foreground_color("darkgray")

RULES = []
f = gui.TextCharFormat()
r = core.RegExp()
r.setMinimal(True)
f.setFontWeight(gui.Font.Normal)
f.set_foreground_color("blue")
tag_list = ["\\btrue\\b", "\\bfalse\\b"]
for tag in tag_list:
    r.setPattern(tag)
    RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.setForeground(gui.Color(127, 64, 127))
r.setPattern(r"\\d+")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.set_foreground_color("darkblue")
r.setPattern(r"^\s*[_.\w]*\s*:")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.set_foreground_color("darkblue")
r.setPattern(r":\s*:[_\.\w]*$|:\s*\@[_\.\w]*$")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.setFontWeight(gui.Font.Bold)
f.set_foreground_color("darkred")
r.setPattern(r"^\s*-")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.set_foreground_color("darkred")
r.setPattern(r"^---$")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.set_foreground_color("darkgreen")
r.setPattern(r"[\[\]\{\}\,]")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.setFontWeight(gui.Font.Normal)
f.set_foreground_color("darkorange")
r.setPattern(r"\".*\"|\'.*\'")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.setForeground(gui.Color(127, 64, 127))
r.setPattern(r"\\$\\(.*\\)")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
f.set_foreground_color("lightgray")
r.setPattern(r"<!DOCTYPE.*>")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))
r.setPattern(r"<\\?xml.*\\?>")
RULES.append((core.RegExp(r), gui.TextCharFormat(f)))


class YamlHighlighter(gui.SyntaxHighlighter):
    """
    Enabled the syntax highlightning for the yaml files.
    """

    def highlightBlock(self, text):
        for pattern, form in RULES:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, form)
                index = pattern.indexIn(text, index + length)
    # mark comment blocks
        self.setCurrentBlockState(0)
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = COMMENT_START.indexIn(text)
            if startIndex >= 0:
                commentLength = len(text) - startIndex
                self.setFormat(startIndex, commentLength, COMMENT_FORMAT)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = YamlHighlighter(editor.document())
    editor.show()
    app.exec_()
