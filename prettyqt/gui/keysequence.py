from __future__ import annotations

from typing import Literal

from prettyqt import constants, qt
from prettyqt.qt import QtGui
from prettyqt.utils import bidict, mappers


SEQUENCE_MATCHES = bidict(
    none=QtGui.QKeySequence.SequenceMatch.NoMatch,
    partial=QtGui.QKeySequence.SequenceMatch.PartialMatch,
    exact=QtGui.QKeySequence.SequenceMatch.ExactMatch,
)

SequenceMatchStr = Literal["none", "partial", "exact"]

SEQUENCE_FORMATS = bidict(
    native=QtGui.QKeySequence.SequenceFormat.NativeText,
    portable=QtGui.QKeySequence.SequenceFormat.PortableText,
)

STANDARD_KEYS = mappers.FlagMap(
    QtGui.QKeySequence.StandardKey,
    add_tab=QtGui.QKeySequence.StandardKey.AddTab,
    back=QtGui.QKeySequence.StandardKey.Back,
    backspace=QtGui.QKeySequence.StandardKey.Backspace,
    bold=QtGui.QKeySequence.StandardKey.Bold,
    close=QtGui.QKeySequence.StandardKey.Close,
    copy=QtGui.QKeySequence.StandardKey.Copy,
    cut=QtGui.QKeySequence.StandardKey.Cut,
    delete=QtGui.QKeySequence.StandardKey.Delete,
    delete_end_of_line=QtGui.QKeySequence.StandardKey.DeleteEndOfLine,
    delete_end_of_word=QtGui.QKeySequence.StandardKey.DeleteEndOfWord,
    delete_start_of_word=QtGui.QKeySequence.StandardKey.DeleteStartOfWord,
    delete_complete_line=QtGui.QKeySequence.StandardKey.DeleteCompleteLine,
    find=QtGui.QKeySequence.StandardKey.Find,
    find_next=QtGui.QKeySequence.StandardKey.FindNext,
    find_previous=QtGui.QKeySequence.StandardKey.FindPrevious,
    forward=QtGui.QKeySequence.StandardKey.Forward,
    help_contents=QtGui.QKeySequence.StandardKey.HelpContents,
    instert_line_separator=QtGui.QKeySequence.StandardKey.InsertLineSeparator,
    insert_paragraph_separator=QtGui.QKeySequence.StandardKey.InsertParagraphSeparator,
    italic=QtGui.QKeySequence.StandardKey.Italic,
    move_to_end_of_block=QtGui.QKeySequence.StandardKey.MoveToEndOfBlock,
    move_to_end_of_document=QtGui.QKeySequence.StandardKey.MoveToEndOfDocument,
    move_to_end_of_line=QtGui.QKeySequence.StandardKey.MoveToEndOfLine,
    move_to_next_char=QtGui.QKeySequence.StandardKey.MoveToNextChar,
    move_to_next_line=QtGui.QKeySequence.StandardKey.MoveToNextLine,
    move_to_next_page=QtGui.QKeySequence.StandardKey.MoveToNextPage,
    move_to_next_word=QtGui.QKeySequence.StandardKey.MoveToNextWord,
    move_to_previous_char=QtGui.QKeySequence.StandardKey.MoveToPreviousChar,
    move_to_previous_line=QtGui.QKeySequence.StandardKey.MoveToPreviousLine,
    move_to_previous_page=QtGui.QKeySequence.StandardKey.MoveToPreviousPage,
    move_to_previous_word=QtGui.QKeySequence.StandardKey.MoveToPreviousWord,
    move_to_start_of_block=QtGui.QKeySequence.StandardKey.MoveToStartOfBlock,
    move_to_start_of_document=QtGui.QKeySequence.StandardKey.MoveToStartOfDocument,
    move_to_start_of_line=QtGui.QKeySequence.StandardKey.MoveToStartOfLine,
    new=QtGui.QKeySequence.StandardKey.New,
    next_child=QtGui.QKeySequence.StandardKey.NextChild,
    open=QtGui.QKeySequence.StandardKey.Open,
    paste=QtGui.QKeySequence.StandardKey.Paste,
    preferences=QtGui.QKeySequence.StandardKey.Preferences,
    previous_child=QtGui.QKeySequence.StandardKey.PreviousChild,
    print=QtGui.QKeySequence.StandardKey.Print,
    quit=QtGui.QKeySequence.StandardKey.Quit,
    redo=QtGui.QKeySequence.StandardKey.Redo,
    refresh=QtGui.QKeySequence.StandardKey.Refresh,
    replace=QtGui.QKeySequence.StandardKey.Replace,
    save_as=QtGui.QKeySequence.StandardKey.SaveAs,
    save=QtGui.QKeySequence.StandardKey.Save,
    select_all=QtGui.QKeySequence.StandardKey.SelectAll,
    deselect=QtGui.QKeySequence.StandardKey.Deselect,
    select_end_of_block=QtGui.QKeySequence.StandardKey.SelectEndOfBlock,
    select_end_of_document=QtGui.QKeySequence.StandardKey.SelectEndOfDocument,
    select_end_of_line=QtGui.QKeySequence.StandardKey.SelectEndOfLine,
    select_next_char=QtGui.QKeySequence.StandardKey.SelectNextChar,
    select_next_line=QtGui.QKeySequence.StandardKey.SelectNextLine,
    select_next_page=QtGui.QKeySequence.StandardKey.SelectNextPage,
    select_next_word=QtGui.QKeySequence.StandardKey.SelectNextWord,
    select_previous_char=QtGui.QKeySequence.StandardKey.SelectPreviousChar,
    select_previous_line=QtGui.QKeySequence.StandardKey.SelectPreviousLine,
    select_previous_page=QtGui.QKeySequence.StandardKey.SelectPreviousPage,
    select_previous_word=QtGui.QKeySequence.StandardKey.SelectPreviousWord,
    select_start_of_block=QtGui.QKeySequence.StandardKey.SelectStartOfBlock,
    select_start_of_document=QtGui.QKeySequence.StandardKey.SelectStartOfDocument,
    select_start_of_line=QtGui.QKeySequence.StandardKey.SelectStartOfLine,
    underline=QtGui.QKeySequence.StandardKey.Underline,
    undo=QtGui.QKeySequence.StandardKey.Undo,
    unknown_key=QtGui.QKeySequence.StandardKey.UnknownKey,
    whats_this=QtGui.QKeySequence.StandardKey.WhatsThis,
    zoom_in=QtGui.QKeySequence.StandardKey.ZoomIn,
    zoom_out=QtGui.QKeySequence.StandardKey.ZoomOut,
    full_screen=QtGui.QKeySequence.StandardKey.FullScreen,
    cancel=QtGui.QKeySequence.StandardKey.Cancel,
)


class KeySequence(QtGui.QKeySequence):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str) and args[0] in STANDARD_KEYS:
            super().__init__(STANDARD_KEYS[args[0]])
        else:
            super().__init__(*args, **kwargs)

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return f"{type(self).__name__}({self.toString()!r})"

    def __bool__(self):
        return not self.isEmpty()

    def __reduce__(self):
        return type(self), (self.toString(),)

    def get_matches(self, seq: QtGui.QKeySequence | str) -> SequenceMatchStr:
        if isinstance(seq, str):
            seq = KeySequence(seq)
        return SEQUENCE_MATCHES.inverse[self.matches(seq)]

    @classmethod
    def to_shortcut_str(cls, key, mod: int = 0) -> str:
        for k, v in constants.MODIFIER_TO_KEY.items():
            if mod & k:  # type: ignore
                key += qt.flag_to_int(v)
        return str(cls(key))


if __name__ == "__main__":
    seq = KeySequence("select_all")
