# -*- coding: utf-8 -*-

import pathlib

from pygments.formatters.html import HtmlFormatter
from pygments.lexer import Error, RegexLexer, Text, _TokenType
from pygments.lexers import get_lexer_by_name, load_lexer_from_file
from pygments.styles import get_style_by_name

from prettyqt import gui


def qstring_length(text):
    """
    Tries to compute what the length of an utf16-encoded QString would be.
    """
    utf16_text = text.encode("utf16")
    length = len(utf16_text) // 2
    # Remove Byte order mark.
    # TODO: All unicode Non-characters should be removed
    if utf16_text[:2] in [b"\xff\xfe", b"\xff\xff", b"\xfe\xff"]:
        length -= 1
    return length


def get_tokens_unprocessed(self, text, stack=("root",)):
    """ Split ``text`` into (tokentype, text) pairs.

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
    while 1:
        for rexmatch, action, new_state in statetokens:
            m = rexmatch(text, pos)
            if not m:
                continue
            if action is not None:
                if type(action) is _TokenType:
                    yield pos, action, m.group()
                else:
                    yield from action(self, m)
            pos = m.end()
            if new_state is None:
                break
            # state transition
            if isinstance(new_state, tuple):
                for state in new_state:
                    if state == "#pop":
                        statestack.pop()
                    elif state == "#push":
                        statestack.append(statestack[-1])
                    else:
                        statestack.append(state)
            elif isinstance(new_state, int):
                # pop
                del statestack[new_state:]
            elif new_state == "#push":
                statestack.append(statestack[-1])
            else:
                assert False, "wrong state def: %r" % new_state
            statetokens = tokendefs[statestack[-1]]
            break
        else:
            try:
                if text[pos] == "\n":
                    # at EOL, reset state to "root"
                    pos += 1
                    statestack = ["root"]
                    statetokens = tokendefs["root"]
                    yield pos, Text, "\n"
                    continue
                yield pos, Error, text[pos]
                pos += 1
            except IndexError:
                break
    self._saved_state_stack = list(statestack)


# Monkeypatch!
RegexLexer.get_tokens_unprocessed = get_tokens_unprocessed


class PygmentsHighlighter(gui.SyntaxHighlighter):
    """ Syntax highlighter that uses Pygments for parsing. """

    # ---------------------------------------------------------------------------
    #  "QSyntaxHighlighter" interface
    # ---------------------------------------------------------------------------

    def __init__(self, parent, lexer=None):
        super().__init__(parent)
        self._document = self.document()
        self._formatter = HtmlFormatter(nowrap=True)
        self.set_style("default")
        if lexer == "regex":
            path = pathlib.Path(__file__).parent
            path = path / "pygments" / "regularexpressionlexer.py"
            self._lexer = load_lexer_from_file(str(path))
        else:
            self._lexer = get_lexer_by_name(lexer)

    def highlightBlock(self, string):
        """ Highlight a block of text.
        """
        prev_data = self.currentBlock().previous().userData()
        if prev_data is not None:
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

    def set_style(self, style):
        """ Sets the style to the specified Pygments style.
        """
        if isinstance(style, str):
            style = get_style_by_name(style)
        self._style = style
        self._clear_caches()

    def set_style_sheet(self, stylesheet):
        """ Sets a CSS stylesheet. The classes in the stylesheet should
        correspond to those generated by:

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
        """ Clear caches for brushes and formats.
        """
        self._brushes = {}
        self._formats = {}

    def _get_format(self, token):
        """ Returns a QTextCharFormat for token or None.
        """
        if token in self._formats:
            return self._formats[token]

        if self._style is None:
            result = self._get_format_from_document(token, self._document)
        else:
            result = self._get_format_from_style(token, self._style)

        self._formats[token] = result
        return result

    def _get_format_from_document(self, token, document):
        """ Returns a QTextCharFormat for token by
        """
        code, html = next(self._formatter._format_lines([(token, "dummy")]))
        self._document.setHtml(html)
        return gui.TextCursor(self._document).charFormat()

    def _get_format_from_style(self, token, style):
        """ Returns a QTextCharFormat for token by reading a Pygments style.
        """
        result = gui.TextCharFormat()
        for key, value in style.style_for_token(token).items():
            if value:
                if key == "color":
                    result.set_foreground_color(self._get_brush(value))
                elif key == "bgcolor":
                    result.set_background_color(self._get_brush(value))
                elif key == "bold":
                    result.set_font_weight("bold")
                elif key == "italic":
                    result.setFontItalic(True)
                elif key == "underline":
                    result.set_underline_style("single")
                elif key == "sans":
                    result.set_font_style_hint("sans_serif")
                elif key == "roman":
                    result.set_font_style_hint("serif")
                elif key == "mono":
                    result.set_font_style_hint("typewriter")
        return result

    def _get_brush(self, color):
        """ Returns a brush for the color.
        """
        result = self._brushes.get(color)
        if result is None:
            qcolor = gui.Color(f"#{color[:6]}")
            result = gui.Brush(qcolor)
            self._brushes[color] = result
        return result


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    editor = widgets.PlainTextEdit()
    highlighter = PygmentsHighlighter(editor.document(), lexer="regex")
    editor.show()
    app.exec_()
