from __future__ import annotations

import functools
import logging
from typing import Literal

from pygments import lexer, lexers, style, styles
from pygments.formatters import html

from prettyqt import core, gui, paths
from prettyqt.utils import get_repr


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


@functools.cache
def _get_brush(color: str) -> gui.Brush:
    """Return a brush for the color."""
    qcolor = gui.Color(f"#{color[:6]}")
    return gui.Brush(qcolor)


def _get_format_from_style(token: str, style: style.Style) -> gui.TextCharFormat:
    """Return a QTextCharFormat for token by reading a Pygments style."""
    result = gui.TextCharFormat()
    try:
        token_style = style.style_for_token(token)
    except KeyError:
        return result
    for key, value in token_style.items():
        if value:
            match key:
                case "color":
                    result.set_foreground_color(_get_brush(value))
                case "bgcolor":
                    result.set_background_color(_get_brush(value))
                case "bold":
                    result.set_font_weight("bold")
                case "italic":
                    result.setFontItalic(True)
                case "underline":
                    result.set_underline_style("single")
                case "sans":
                    result.set_font_style_hint("sans_serif")
                case "roman":
                    result.set_font_style_hint("serif")
                case "mono":
                    result.set_font_style_hint("typewriter")
    return result


def qstring_length(text: str) -> int:
    """Tries to compute what the length of an utf16-encoded QString would be."""
    utf16_text = text.encode("utf16")
    length = len(utf16_text) // 2
    # Remove Byte order mark.
    # TODO: All unicode Non-characters should be removed
    if utf16_text[:2] in [b"\xff\xfe", b"\xff\xff", b"\xfe\xff"]:
        length -= 1
    return length


def get_tokens_unprocessed(self, text: str, stack=("root",)):
    """Split ``text`` into (tokentype, text) pairs.

    Monkeypatched to store the final stack on the object itself.

    The `text` parameter this gets passed is only the current line, so to
    highlight things like multiline strings correctly, we need to retrieve
    the state from the previous line (this is done in PygmentsHighlighter,
    below), and use it to continue processing the current line.
    """
    pos = 0
    tokendefs = self._tokens
    if hasattr(self, "_saved_state_stack"):
        statestack = list(self._saved_state_stack)
    else:
        statestack = list(stack)
    statetokens = tokendefs[statestack[-1]]
    while True:
        for rexmatch, action, new_state in statetokens:
            m = rexmatch(text, pos)
            if not m:
                continue
            if action is not None:
                if isinstance(action, lexer._TokenType):
                    yield pos, action, m.group()
                else:
                    yield from action(self, m)
            pos = m.end()
            match new_state:
                case None:
                    break
                case tuple():
                    for state in new_state:
                        match state:
                            case "#pop":
                                statestack.pop()
                            case "#push":
                                statestack.append(statestack[-1])
                            case _:
                                statestack.append(state)
                case int():
                    del statestack[new_state:]
                case "#push":
                    statestack.append(statestack[-1])
                case _:
                    msg = f"wrong state def: {new_state!r}"
                    raise AssertionError(msg)
            statetokens = tokendefs[statestack[-1]]
            break
        else:
            try:
                if text[pos] == "\n":
                    # at EOL, reset state to "root"
                    statestack = ["root"]
                    statetokens = tokendefs["root"]
                    yield pos + 1, lexer.Text, "\n"
                else:
                    yield pos, lexer.Error, text[pos]
                pos += 1
            except IndexError:
                break
    self._saved_state_stack = list(statestack)


# Monkeypatch!
lexer.RegexLexer.get_tokens_unprocessed = get_tokens_unprocessed


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
        self._formatter = html.HtmlFormatter(nowrap=True)
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

    def __repr__(self):
        return get_repr(self, lexer=self._lexer.aliases[0])

    def highlightBlock(self, string):
        """Highlight a block of text."""
        if (prev_data := self.currentBlock().previous().userData()) is not None:
            self._lexer._saved_state_stack = prev_data.syntax_stack
        elif hasattr(self._lexer, "_saved_state_stack"):
            del self._lexer._saved_state_stack

        # Lex the text using Pygments
        index = 0
        for token, text in self._lexer.get_tokens(string):
            length = qstring_length(text)
            self.setFormat(index, length, self._get_format(token))
            index += length

        if hasattr(self._lexer, "_saved_state_stack"):
            data = gui.TextBlockUserData(syntax_stack=self._lexer._saved_state_stack)
            self.currentBlock().setUserData(data)
            # Clean up for the next go-round.
            del self._lexer._saved_state_stack

    # ---------------------------------------------------------------------------
    # "PygmentsHighlighter" interface
    # ---------------------------------------------------------------------------

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
        self._clear_caches()

    def get_style(self) -> StyleStr:
        return self._stylename

    def adjust_style_to_palette(self):
        pal = gui.GuiApplication.get_palette()
        style = "monokai" if pal.is_dark() else "default"
        self.set_style(style)

    def set_style_sheet(self, stylesheet: str):
        """Sets a CSS stylesheet.

        The classes in the stylesheet should correspond to those generated by:

            pygmentize -S <style> -f html

        Note that "set_style" and "set_style_sheet" completely override each
        other, i.e. they cannot be used in conjunction.
        """
        self._document.setDefaultStyleSheet(stylesheet)
        self._style = None
        self._clear_caches()

    # ---------------------------------------------------------------------------
    # Protected interface
    # ---------------------------------------------------------------------------

    def _clear_caches(self):
        """Clear caches for brushes and formats."""
        _get_brush.cache_clear()
        self._get_format.cache_clear()

    @functools.cache  # noqa: B019
    def _get_format(self, token: str) -> gui.QTextCharFormat:
        """Returns a QTextCharFormat for token or None."""
        if self._style is None:
            return self._get_format_from_document(token, self._document)
        return _get_format_from_style(token, self._style)

    def _get_format_from_document(
        self, token: str, document: gui.QTextDocument
    ) -> gui.QTextCharFormat:
        """Return a QTextCharFormat for token from document."""
        _, html = next(self._formatter._format_lines([(token, "dummy")]))
        document.setHtml(html)
        return gui.TextCursor(document).charFormat()

    style = core.Property(
        str,
        get_style,
        set_style,
        doc="Pygments style for the highlighter",
    )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    app.set_style("Fusion")
    editor = widgets.PlainTextEdit()
    highlighter = PygmentsHighlighter(editor.document(), lexer="python")
    # highlighter.set_style("monokai")
    editor.show()
    app.exec()
