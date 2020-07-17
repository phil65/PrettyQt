# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from typing import Optional

from PyQt5 import Qsci  # type: ignore

from prettyqt import gui, widgets
from prettyqt.utils import colors, bidict

ARROW_MARKER_NUM = 8

MATCH_TYPES = bidict(
    none=Qsci.QsciScintilla.NoBraceMatch,
    strict=Qsci.QsciScintilla.StrictBraceMatch,
    sloppy=Qsci.QsciScintilla.SloppyBraceMatch,
)

LEXERS = bidict(
    bash=Qsci.QsciLexerBash,
    batch=Qsci.QsciLexerBatch,
    cmake=Qsci.QsciLexerCMake,
    cpp=Qsci.QsciLexerCPP,
    css=Qsci.QsciLexerCSS,
    csharp=Qsci.QsciLexerCSharp,
    coffeescript=Qsci.QsciLexerCoffeeScript,
    d=Qsci.QsciLexerD,
    diff=Qsci.QsciLexerDiff,
    fortran=Qsci.QsciLexerFortran,
    fortran77=Qsci.QsciLexerFortran77,
    html=Qsci.QsciLexerHTML,
    java=Qsci.QsciLexerJava,
    javascript=Qsci.QsciLexerJavaScript,
    lua=Qsci.QsciLexerLua,
    makefile=Qsci.QsciLexerMakefile,
    matlab=Qsci.QsciLexerMatlab,
    octave=Qsci.QsciLexerOctave,
    po=Qsci.QsciLexerPO,
    pov=Qsci.QsciLexerPOV,
    pascal=Qsci.QsciLexerPascal,
    perl=Qsci.QsciLexerPerl,
    postscript=Qsci.QsciLexerPostScript,
    properties=Qsci.QsciLexerProperties,
    ruby=Qsci.QsciLexerRuby,
    spice=Qsci.QsciLexerSpice,
    tcl=Qsci.QsciLexerTCL,
    tex=Qsci.QsciLexerTeX,
    vhdl=Qsci.QsciLexerVHDL,
    verilog=Qsci.QsciLexerVerilog,
    xml=Qsci.QsciLexerXML,
    python=Qsci.QsciLexerPython,
    yaml=Qsci.QsciLexerYAML,
    json=Qsci.QsciLexerJSON,
    sql=Qsci.QsciLexerSQL,
    markdown=Qsci.QsciLexerMarkdown,
    idl=Qsci.QsciLexerIDL,
)

MARKERS = bidict(
    circle=Qsci.QsciScintilla.Circle,
    rectangle=Qsci.QsciScintilla.Rectangle,
    right_triangle=Qsci.QsciScintilla.RightTriangle,
    small_rectangle=Qsci.QsciScintilla.SmallRectangle,
    right_arrow=Qsci.QsciScintilla.RightArrow,
    invisible=Qsci.QsciScintilla.Invisible,
    down_triangle=Qsci.QsciScintilla.DownTriangle,
    minus=Qsci.QsciScintilla.Minus,
    plus=Qsci.QsciScintilla.Plus,
    vertical_line=Qsci.QsciScintilla.VerticalLine,
    bottom_left_corner=Qsci.QsciScintilla.BottomLeftCorner,
    left_side_splitter=Qsci.QsciScintilla.LeftSideSplitter,
    boxed_plus=Qsci.QsciScintilla.BoxedPlus,
    boxed_plus_connected=Qsci.QsciScintilla.BoxedPlusConnected,
    boxed_minus=Qsci.QsciScintilla.BoxedMinus,
    boxed_minus_connected=Qsci.QsciScintilla.BoxedMinusConnected,
    rounded_bottom_left_corner=Qsci.QsciScintilla.RoundedBottomLeftCorner,
    left_side_rounded_splitter=Qsci.QsciScintilla.LeftSideRoundedSplitter,
    circled_plus=Qsci.QsciScintilla.CircledPlus,
    circled_plus_connected=Qsci.QsciScintilla.CircledPlusConnected,
    circled_minus=Qsci.QsciScintilla.CircledMinus,
    circled_minus_connected=Qsci.QsciScintilla.CircledMinusConnected,
    background=Qsci.QsciScintilla.Background,
    three_dots=Qsci.QsciScintilla.ThreeDots,
    three_right_arrows=Qsci.QsciScintilla.ThreeRightArrows,
    full_rectangle=Qsci.QsciScintilla.FullRectangle,
    left_rectangle=Qsci.QsciScintilla.LeftRectangle,
    underline=Qsci.QsciScintilla.Underline,
    bookmark=Qsci.QsciScintilla.Bookmark,
)

WRAP_MODES = bidict(
    none=Qsci.QsciScintilla.WrapNone,
    word=Qsci.QsciScintilla.WrapWord,
    anywhere=Qsci.QsciScintilla.WrapCharacter,
    whitespace=Qsci.QsciScintilla.WrapWhitespace,
)

Qsci.QsciScintilla.__bases__[0].__bases__ = (widgets.AbstractScrollArea,)


class SciScintilla(Qsci.QsciScintilla):
    supported_langs = LEXERS.keys()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the default font
        font = gui.Font("Consolas")
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        self.setMarginWidth(0, font.metrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.set_margins_background_color("lightgrey")

        # Clickable margin 1 for showing markers
        # self.setMarginSensitivity(1, True)
        # self.marginClicked.connect(self.on_margin_clicked)
        # self.define_marker("right_arrow", ARROW_MARKER_NUM)
        # self.set_marker_background_color("red", ARROW_MARKER_NUM)
        self.set_brace_matching("sloppy")
        self.highlight_current_line()

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        # self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.SendScintilla(self.SCI_SETSCROLLWIDTHTRACKING, True)
        self.SendScintilla(self.SCI_SETSCROLLWIDTH, 5)
        self.language = None
        self._lexer = None

    def set_marker_background_color(self, color: colors.ColorType, marker_num):
        self.setMarkerBackgroundColor(colors.get_color(color), marker_num)

    def set_margins_background_color(self, color: colors.ColorType):
        self.setMarginsBackgroundColor(colors.get_color(color))

    def highlight_current_line(self, color: colors.ColorType = "yellow"):
        self.setCaretLineVisible(color is not None)
        self.setCaretLineBackgroundColor(colors.get_color(color))

    def set_brace_matching(self, match_type: Optional[str]):
        if match_type is None:
            match_type = "none"
        if match_type not in MATCH_TYPES:
            raise ValueError(f"Invalid match type '{match_type}.")
        self.setBraceMatching(MATCH_TYPES[match_type])

    def define_marker(self, marker: str, num: int):
        if marker not in MARKERS:
            raise ValueError(f"Invalid marker '{marker}.")
        self.markerDefine(MARKERS[marker], num)

    def set_text(self, text: str):
        self.setText(text)

    def set_syntaxhighlighter(self, language: str):
        self.language = language
        font = gui.Font.mono()
        self._lexer = LEXERS[language]()
        self._lexer.setDefaultFont(font)
        self._lexer.setFont(font)
        self.setLexer(self._lexer)

    def scroll_to_bottom(self):
        self.ensureLineVisible(self.lines())

    def append_text(self, text: str, newline: bool = True):
        if newline:
            self.append("\n" + text)
        else:
            self.append(text)

    def set_font(self, font):
        self.setFont(font)
        self.setMarginsFont(font)
        lexer = self._lexer
        if lexer is not None:
            lexer.setDefaultFont(font)
            lexer.setFont(font)
            self.setLexer(lexer)

    def set_read_only(self, value: bool = True):
        self.setReadOnly(value)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        self.toggle_marker(nline, ARROW_MARKER_NUM)

    def toggle_marker(self, nline: int, marker_num: int):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, marker_num)
        else:
            self.markerAdd(nline, marker_num)

    def set_wrap_mode(self, mode: Optional[str]):
        if mode is None:
            mode = "none"
        if mode not in WRAP_MODES:
            raise ValueError(f"Invalid wrap mode '{mode}.")
        self.setWrapMode(WRAP_MODES[mode])

    def get_value(self) -> str:
        return self.text()

    def set_value(self, value: str):
        self.setText(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = SciScintilla()
    widget.set_syntaxhighlighter("python")
    widget.set_wrap_mode("anywhere")
    widget.show()
    app.exec_()
