# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import gui, core


class YamlHighlighter(gui.SyntaxHighlighter):
    """
    Enabled the syntax highlightning for the yaml files.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []
        self.commentStart = core.RegExp("#")
        self.commentEnd = core.RegExp("\n|\r")
        self.commentFormat = gui.TextCharFormat()
        self.commentFormat.setFontItalic(True)
        self.commentFormat.set_foreground_color("darkgray")
        f = gui.TextCharFormat()
        r = core.RegExp()
        r.setMinimal(True)
        f.setFontWeight(gui.Font.Normal)
        f.set_foreground_color("blue")
        tag_list = ["\\btrue\\b", "\\bfalse\\b"]
        for tag in tag_list:
            r.setPattern(tag)
            self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(gui.Color(127, 64, 127))
        r.setPattern("\\d+")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.set_foreground_color("darkblue")
        r.setPattern("^\s*[_.\w]*\s*:")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.set_foreground_color("darkblue")
        r.setPattern(":\s*:[_\.\w]*$|:\s*\@[_\.\w]*$")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setFontWeight(gui.Font.Bold)
        f.set_foreground_color("darkred")
        r.setPattern("^\s*-")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.set_foreground_color("darkred")
        r.setPattern("^---$")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.set_foreground_color("darkgreen")
        r.setPattern("[\[\]\{\}\,]")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setFontWeight(gui.Font.Normal)
        f.set_foreground_color("magenta")
        r.setPattern("\".*\"|\'.*\'")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(gui.Color(127, 64, 127))
        r.setPattern("\\$\\(.*\\)")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.set_foreground_color("lightgray")
        r.setPattern("<!DOCTYPE.*>")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        r.setPattern("<\\?xml.*\\?>")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
