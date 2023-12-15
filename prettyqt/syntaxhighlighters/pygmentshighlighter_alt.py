from __future__ import annotations

import contextlib
from itertools import takewhile
import logging
from typing import Literal

from pygments import highlight, lexers, styles
from pygments.formatter import Formatter

from prettyqt import core, gui, paths
from prettyqt.utils import get_repr


# inspired by  https://github.com/Vector35/snippets/blob/master/QCodeEditor.py
# (MIT license) and
# https://pygments.org/docs/formatterdevelopment/#html-3-2-formatter

logger = logging.getLogger(__name__)


StyleStr = Literal[
    "default",
    "emacs",
    "friendly",
    "friendly_grayscale",
    "colorful",
    "autumn",
    "murphy",
    "manni",
    "material",
    "monokai",
    "perldoc",
    "pastie",
    "borland",
    "trac",
    "native",
    "fruity",
    "bw",
    "vim",
    "vs",
    "tango",
    "rrt",
    "xcode",
    "igor",
    "paraiso-light",
    "paraiso-dark",
    "lovelace",
    "algol",
    "algol_nu",
    "arduino",
    "rainbow_dash",
    "abap",
    "solarized-dark",
    "solarized-light",
    "sas",
    "staroffice",
    "stata",
    "stata-light",
    "stata-dark",
    "inkpot",
    "zenburn",
    "gruvbox-dark",
    "gruvbox-light",
    "dracula",
    "one-dark",
    "lilypond",
    "nord",
    "nord-darker",
    "github-dark",
]


class PygmentsHighlighter(gui.SyntaxHighlighter):
    """Syntax highlighter that uses Pygments for parsing."""

    # ---------------------------------------------------------------------------
    #  "QSyntaxHighlighter" interface
    # ---------------------------------------------------------------------------

    def __init__(
        self,
        parent: gui.QTextDocument,
        lexer: str,
        style: None | StyleStr = None,
    ):
        super().__init__(parent)

        self._document = self.document()
        self._style = None
        self._stylename = ""
        if style is None:
            gui.GuiApplication.styleHints().colorSchemeChanged.connect(
                self.adjust_style_to_palette
            )
        self.set_style(style)
        if lexer == "regex":
            self._lexer = lexers.load_lexer_from_file(str(paths.RE_LEXER_PATH))
        else:
            self._lexer = lexers.get_lexer_by_name(lexer)
        self._formatter = QFormatter(style=self._stylename)

    @property
    def background_color(self):
        return self._formatter.style.background_color

    def highlightBlock(self, text):
        cb = self.currentBlock()
        p = cb.position()
        text_ = self.document().toPlainText() + "\n"
        highlight(text_, self._lexer, self._formatter)

        enters = sum(1 for _ in takewhile(lambda x: x == "\n", text_))
        # pygments lexer ignore leading empty lines, so we need to do correction
        # here calculating the number of empty lines.

        # dirty, dirty hack
        # The core problem is that pygemnts by default use string streams,
        # that will not handle QTextCharFormat, so we need use `data` property to
        # work around this.
        for i in range(len(text)):
            with contextlib.suppress(IndexError):
                self.setFormat(i, 1, self._formatter.data[p + i - enters])

    def __repr__(self):
        return get_repr(self, lexer=self._lexer.aliases[0])

    def set_style(self, style: None | StyleStr):
        match style:
            case None:
                self.adjust_style_to_palette()
                return
            case str():
                self._style = styles.get_style_by_name(style)
                self._stylename = style
            case _:
                raise TypeError(style)
        self._formatter = QFormatter(style=self._stylename)

    def get_style(self) -> StyleStr:
        return self._stylename

    def adjust_style_to_palette(self):
        pal = gui.GuiApplication.get_palette()
        style = "monokai" if pal.is_dark() else "default"
        self.set_style(style)

    style = core.Property(
        str,
        get_style,
        set_style,
        doc="Pygments style for the highlighter",
    )


def get_text_char_format(style):
    text_char_format = gui.QTextCharFormat()
    if hasattr(text_char_format, "setFontFamilies"):
        text_char_format.setFontFamilies(["monospace"])
    else:
        text_char_format.setFontFamily("monospace")
    if style.get("color"):
        text_char_format.setForeground(gui.QColor(f"#{style['color']}"))

    if style.get("bgcolor"):
        text_char_format.setBackground(gui.QColor(style["bgcolor"]))

    if style.get("bold"):
        text_char_format.setFontWeight(gui.QFont.Weight.Bold)
    if style.get("italic"):
        text_char_format.setFontItalic(True)
    if style.get("underline"):
        text_char_format.setFontUnderline(True)

    # TODO find if it is possible to support border style.

    return text_char_format


class QFormatter(Formatter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self._style = {name: get_text_char_format(style) for name, style in self.style}

    def format(self, tokensource, outfile):
        """Format the given token stream.

        `outfile` is argument from parent class, but
        in Qt we do not produce string output, but QTextCharFormat, so it needs to be
        collected using `self.data`.
        """
        self.data = []

        for token, value in tokensource:
            self.data.extend([self._style[token]] * len(value))


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    app.set_style("Fusion")
    editor = widgets.PlainTextEdit()
    highlighter = PygmentsHighlighter(editor.document(), lexer="python")
    # highlighter.set_style("monokai")
    editor.show()
    app.exec()
