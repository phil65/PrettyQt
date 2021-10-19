from __future__ import annotations

from typing import Literal

from prettyqt import gui, widgets
from prettyqt.qt import Qsci, QtGui  # type: ignore
from prettyqt.utils import InvalidParamError, bidict, colors, types


ARROW_MARKER_NUM = 8

MATCH_TYPE = bidict(
    none=Qsci.QsciScintilla.BraceMatch.NoBraceMatch,
    strict=Qsci.QsciScintilla.BraceMatch.StrictBraceMatch,
    sloppy=Qsci.QsciScintilla.BraceMatch.SloppyBraceMatch,
)

MatchTypeStr = Literal["none", "strict", "sloppy"]

LEXER = bidict(
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

LexerStr = Literal[
    "bash",
    "batch",
    "cmake",
    "cpp",
    "css",
    "csharp",
    "coffeescript",
    "d",
    "diff",
    "fortran",
    "fortran77",
    "html",
    "java",
    "javascript",
    "lua",
    "makefile",
    "matlab",
    "octave",
    "po",
    "pov",
    "pascal",
    "perl",
    "postscript",
    "properties",
    "ruby",
    "spice",
    "tcl",
    "tex",
    "vhdl",
    "verilog",
    "xml",
    "python",
    "yaml",
    "json",
    "sql",
    "markdown",
    "idl",
]

MARKER = bidict(
    circle=Qsci.QsciScintilla.MarkerSymbol.Circle,
    rectangle=Qsci.QsciScintilla.MarkerSymbol.Rectangle,
    right_triangle=Qsci.QsciScintilla.MarkerSymbol.RightTriangle,
    small_rectangle=Qsci.QsciScintilla.MarkerSymbol.SmallRectangle,
    right_arrow=Qsci.QsciScintilla.MarkerSymbol.RightArrow,
    invisible=Qsci.QsciScintilla.MarkerSymbol.Invisible,
    down_triangle=Qsci.QsciScintilla.MarkerSymbol.DownTriangle,
    minus=Qsci.QsciScintilla.MarkerSymbol.Minus,
    plus=Qsci.QsciScintilla.MarkerSymbol.Plus,
    vertical_line=Qsci.QsciScintilla.MarkerSymbol.VerticalLine,
    bottom_left_corner=Qsci.QsciScintilla.MarkerSymbol.BottomLeftCorner,
    left_side_splitter=Qsci.QsciScintilla.MarkerSymbol.LeftSideSplitter,
    boxed_plus=Qsci.QsciScintilla.MarkerSymbol.BoxedPlus,
    boxed_plus_connected=Qsci.QsciScintilla.MarkerSymbol.BoxedPlusConnected,
    boxed_minus=Qsci.QsciScintilla.MarkerSymbol.BoxedMinus,
    boxed_minus_connected=Qsci.QsciScintilla.MarkerSymbol.BoxedMinusConnected,
    rounded_bottom_left_corner=Qsci.QsciScintilla.MarkerSymbol.RoundedBottomLeftCorner,
    left_side_rounded_splitter=Qsci.QsciScintilla.MarkerSymbol.LeftSideRoundedSplitter,
    circled_plus=Qsci.QsciScintilla.MarkerSymbol.CircledPlus,
    circled_plus_connected=Qsci.QsciScintilla.MarkerSymbol.CircledPlusConnected,
    circled_minus=Qsci.QsciScintilla.MarkerSymbol.CircledMinus,
    circled_minus_connected=Qsci.QsciScintilla.MarkerSymbol.CircledMinusConnected,
    background=Qsci.QsciScintilla.MarkerSymbol.Background,
    three_dots=Qsci.QsciScintilla.MarkerSymbol.ThreeDots,
    three_right_arrows=Qsci.QsciScintilla.MarkerSymbol.ThreeRightArrows,
    full_rectangle=Qsci.QsciScintilla.MarkerSymbol.FullRectangle,
    left_rectangle=Qsci.QsciScintilla.MarkerSymbol.LeftRectangle,
    underline=Qsci.QsciScintilla.MarkerSymbol.Underline,
    bookmark=Qsci.QsciScintilla.MarkerSymbol.Bookmark,
)

MarkerStr = Literal[
    "circle",
    "rectangle",
    "right_triangle",
    "small_rectangle",
    "right_arrow",
    "invisible",
    "down_triangle",
    "minus",
    "plus",
    "vertical_line",
    "bottom_left_corner",
    "left_side_splitter",
    "boxed_plus",
    "boxed_plus_connected",
    "boxed_minus",
    "boxed_minus_connected",
    "rounded_bottom_left_corner",
    "left_side_rounded_splitter",
    "circled_plus",
    "circled_plus_connected",
    "circled_minus",
    "circled_minus_connected",
    "background",
    "three_dots",
    "three_right_arrows",
    "full_rectangle",
    "left_rectangle",
    "underline",
    "bookmark",
]

WRAP_MODE = bidict(
    none=Qsci.QsciScintilla.WrapMode.WrapNone,
    word=Qsci.QsciScintilla.WrapMode.WrapWord,
    anywhere=Qsci.QsciScintilla.WrapMode.WrapCharacter,
    whitespace=Qsci.QsciScintilla.WrapMode.WrapWhitespace,
)

WrapModeStr = Literal["none", "word", "anywhere", "whitespace"]

Qsci.QsciScintilla.__bases__[0].__bases__ = (widgets.AbstractScrollArea,)


class SciScintilla(Qsci.QsciScintilla):
    supported_langs = LEXER.keys()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the default font
        font = gui.Font("Consolas")
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        self.setMarginWidth(0, font.metrics.horizontalAdvance("00000") + 6)
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

    def set_marker_background_color(self, color: types.ColorType, marker_num):
        self.setMarkerBackgroundColor(colors.get_color(color), marker_num)

    def set_margins_background_color(self, color: types.ColorType):
        self.setMarginsBackgroundColor(colors.get_color(color))

    def highlight_current_line(self, color: types.ColorType = None):
        if color is None:
            color = self.get_palette().get_color("highlight")
        else:
            color = colors.get_color(color)
        self.setCaretLineVisible(color is not None)
        self.setCaretLineBackgroundColor(color)

    def set_brace_matching(self, match_type: MatchTypeStr | None):
        if match_type is None:
            match_type = "none"
        if match_type not in MATCH_TYPE:
            raise InvalidParamError(match_type, MATCH_TYPE)
        self.setBraceMatching(MATCH_TYPE[match_type])

    def define_marker(self, marker: MarkerStr, num: int):
        if marker not in MARKER:
            raise InvalidParamError(marker, MARKER)
        self.markerDefine(MARKER[marker], num)

    def set_text(self, text: str):
        self.setText(text)

    def set_syntaxhighlighter(self, language: LexerStr):
        self.language = language
        font = gui.Font.mono()
        self._lexer = LEXER[language]()
        self._lexer.setDefaultFont(font)
        self._lexer.setFont(font)
        self.setLexer(self._lexer)

    def scroll_to_bottom(self):
        self.ensureLineVisible(self.lines())

    def append_text(self, text: str, newline: bool = True):
        self.append(f"\n{text}" if newline else text)

    def set_font(self, font: QtGui.QFont):
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

    def set_wrap_mode(self, mode: WrapModeStr | None):
        if mode is None:
            mode = "none"
        if mode not in WRAP_MODE:
            raise InvalidParamError(mode, WRAP_MODE)
        self.setWrapMode(WRAP_MODE[mode])

    def get_value(self) -> str:
        return self.text()

    def set_value(self, value: str):
        self.setText(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = SciScintilla()
    widget.set_syntaxhighlighter("python")
    widget.highlight_current_line()
    widget.set_wrap_mode("anywhere")
    widget.show()
    app.main_loop()
