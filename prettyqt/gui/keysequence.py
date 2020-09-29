# -*- coding: utf-8 -*-

from qtpy import QtCore, QtGui

from prettyqt.utils import bidict


SEQUENCE_MATCHES = bidict(
    none=QtGui.QKeySequence.NoMatch,
    partial=QtGui.QKeySequence.PartialMatch,
    exact=QtGui.QKeySequence.ExactMatch,
)

SEQUENCE_FORMATS = bidict(
    native=QtGui.QKeySequence.NativeText,
    portable=QtGui.QKeySequence.PortableText,
)

MODS = {
    QtCore.Qt.ShiftModifier: QtCore.Qt.SHIFT,
    QtCore.Qt.ControlModifier: QtCore.Qt.CTRL,
    QtCore.Qt.AltModifier: QtCore.Qt.ALT,
    QtCore.Qt.MetaModifier: QtCore.Qt.META,
}

STANDARD_KEYS = bidict(
    add_tab=QtGui.QKeySequence.AddTab,
    back=QtGui.QKeySequence.Back,
    backspace=QtGui.QKeySequence.Backspace,
    bold=QtGui.QKeySequence.Bold,
    close=QtGui.QKeySequence.Close,
    copy=QtGui.QKeySequence.Copy,
    cut=QtGui.QKeySequence.Cut,
    delete=QtGui.QKeySequence.Delete,
    delete_end_of_line=QtGui.QKeySequence.DeleteEndOfLine,
    delete_end_of_word=QtGui.QKeySequence.DeleteEndOfWord,
    delete_start_of_word=QtGui.QKeySequence.DeleteStartOfWord,
    delete_complete_line=QtGui.QKeySequence.DeleteCompleteLine,
    find=QtGui.QKeySequence.Find,
    find_next=QtGui.QKeySequence.FindNext,
    find_previous=QtGui.QKeySequence.FindPrevious,
    forward=QtGui.QKeySequence.Forward,
    help_contents=QtGui.QKeySequence.HelpContents,
    instert_line_separator=QtGui.QKeySequence.InsertLineSeparator,
    insert_paragraph_separator=QtGui.QKeySequence.InsertParagraphSeparator,
    italic=QtGui.QKeySequence.Italic,
    move_to_end_of_block=QtGui.QKeySequence.MoveToEndOfBlock,
    move_to_end_of_document=QtGui.QKeySequence.MoveToEndOfDocument,
    move_to_end_of_line=QtGui.QKeySequence.MoveToEndOfLine,
    move_to_next_char=QtGui.QKeySequence.MoveToNextChar,
    move_to_next_line=QtGui.QKeySequence.MoveToNextLine,
    move_to_next_page=QtGui.QKeySequence.MoveToNextPage,
    move_to_next_word=QtGui.QKeySequence.MoveToNextWord,
    move_to_previous_char=QtGui.QKeySequence.MoveToPreviousChar,
    move_to_previous_line=QtGui.QKeySequence.MoveToPreviousLine,
    move_to_previous_page=QtGui.QKeySequence.MoveToPreviousPage,
    move_to_previous_word=QtGui.QKeySequence.MoveToPreviousWord,
    move_to_start_of_block=QtGui.QKeySequence.MoveToStartOfBlock,
    move_to_start_of_document=QtGui.QKeySequence.MoveToStartOfDocument,
    move_to_start_of_line=QtGui.QKeySequence.MoveToStartOfLine,
    new=QtGui.QKeySequence.New,
    next_child=QtGui.QKeySequence.NextChild,
    open=QtGui.QKeySequence.Open,
    paste=QtGui.QKeySequence.Paste,
    preferences=QtGui.QKeySequence.Preferences,
    previous_child=QtGui.QKeySequence.PreviousChild,
    print=QtGui.QKeySequence.Print,
    quit=QtGui.QKeySequence.Quit,
    redo=QtGui.QKeySequence.Redo,
    refresh=QtGui.QKeySequence.Refresh,
    replace=QtGui.QKeySequence.Replace,
    save_as=QtGui.QKeySequence.SaveAs,
    save=QtGui.QKeySequence.Save,
    select_all=QtGui.QKeySequence.SelectAll,
    deselect=QtGui.QKeySequence.Deselect,
    select_end_of_block=QtGui.QKeySequence.SelectEndOfBlock,
    select_end_of_document=QtGui.QKeySequence.SelectEndOfDocument,
    select_end_of_line=QtGui.QKeySequence.SelectEndOfLine,
    select_next_char=QtGui.QKeySequence.SelectNextChar,
    select_next_line=QtGui.QKeySequence.SelectNextLine,
    select_next_page=QtGui.QKeySequence.SelectNextPage,
    select_next_word=QtGui.QKeySequence.SelectNextWord,
    select_previous_char=QtGui.QKeySequence.SelectPreviousChar,
    select_previous_line=QtGui.QKeySequence.SelectPreviousLine,
    select_previous_page=QtGui.QKeySequence.SelectPreviousPage,
    select_previous_word=QtGui.QKeySequence.SelectPreviousWord,
    select_start_of_block=QtGui.QKeySequence.SelectStartOfBlock,
    select_start_of_document=QtGui.QKeySequence.SelectStartOfDocument,
    select_start_of_line=QtGui.QKeySequence.SelectStartOfLine,
    underline=QtGui.QKeySequence.Underline,
    undo=QtGui.QKeySequence.Undo,
    unknown_key=QtGui.QKeySequence.UnknownKey,
    whats_this=QtGui.QKeySequence.WhatsThis,
    zoom_in=QtGui.QKeySequence.ZoomIn,
    zoom_out=QtGui.QKeySequence.ZoomOut,
    full_screen=QtGui.QKeySequence.FullScreen,
    cancel=QtGui.QKeySequence.Cancel,
)


class KeySequence(QtGui.QKeySequence):
    def __str__(self):
        return self.toString()

    def __repr__(self):
        return f"KeySequence({self.toString()!r})"

    def __bool__(self):
        return not self.isEmpty()

    def __reduce__(self):
        return (self.__class__, (self.toString(),))

    def get_matches(self, seq):
        if isinstance(seq, str):
            seq = KeySequence(seq)
        return SEQUENCE_MATCHES.inv[self.matches(seq)]

    @classmethod
    def to_shortcut_str(cls, key, mod=0):
        for k, v in MODS.items():
            if mod & k:
                key += v
        return str(cls(key))
