from typing import Union

from qtpy import QtCore, QtGui

from prettyqt.utils import bidict


SEQUENCE_MATCHES = bidict(
    none=QtGui.QKeySequence.NoMatch,
    partial=QtGui.QKeySequence.PartialMatch,
    exact=QtGui.QKeySequence.ExactMatch,
)

SEQUENCE_FORMATS = bidict(
    native=QtGui.QKeySequence.NativeText, portable=QtGui.QKeySequence.PortableText
)

MODS = {
    QtCore.Qt.ShiftModifier: QtCore.Qt.SHIFT,
    QtCore.Qt.ControlModifier: QtCore.Qt.CTRL,
    QtCore.Qt.AltModifier: QtCore.Qt.ALT,
    QtCore.Qt.MetaModifier: QtCore.Qt.META,
}

STANDARD_KEYS = bidict(
    add_tab=int(QtGui.QKeySequence.AddTab),
    back=int(QtGui.QKeySequence.Back),
    backspace=int(QtGui.QKeySequence.Backspace),
    bold=int(QtGui.QKeySequence.Bold),
    close=int(QtGui.QKeySequence.Close),
    copy=int(QtGui.QKeySequence.Copy),
    cut=int(QtGui.QKeySequence.Cut),
    delete=int(QtGui.QKeySequence.Delete),
    delete_end_of_line=int(QtGui.QKeySequence.DeleteEndOfLine),
    delete_end_of_word=int(QtGui.QKeySequence.DeleteEndOfWord),
    delete_start_of_word=int(QtGui.QKeySequence.DeleteStartOfWord),
    delete_complete_line=int(QtGui.QKeySequence.DeleteCompleteLine),
    find=int(QtGui.QKeySequence.Find),
    find_next=int(QtGui.QKeySequence.FindNext),
    find_previous=int(QtGui.QKeySequence.FindPrevious),
    forward=int(QtGui.QKeySequence.Forward),
    help_contents=int(QtGui.QKeySequence.HelpContents),
    instert_line_separator=int(QtGui.QKeySequence.InsertLineSeparator),
    insert_paragraph_separator=int(QtGui.QKeySequence.InsertParagraphSeparator),
    italic=int(QtGui.QKeySequence.Italic),
    move_to_end_of_block=int(QtGui.QKeySequence.MoveToEndOfBlock),
    move_to_end_of_document=int(QtGui.QKeySequence.MoveToEndOfDocument),
    move_to_end_of_line=int(QtGui.QKeySequence.MoveToEndOfLine),
    move_to_next_char=int(QtGui.QKeySequence.MoveToNextChar),
    move_to_next_line=int(QtGui.QKeySequence.MoveToNextLine),
    move_to_next_page=int(QtGui.QKeySequence.MoveToNextPage),
    move_to_next_word=int(QtGui.QKeySequence.MoveToNextWord),
    move_to_previous_char=int(QtGui.QKeySequence.MoveToPreviousChar),
    move_to_previous_line=int(QtGui.QKeySequence.MoveToPreviousLine),
    move_to_previous_page=int(QtGui.QKeySequence.MoveToPreviousPage),
    move_to_previous_word=int(QtGui.QKeySequence.MoveToPreviousWord),
    move_to_start_of_block=int(QtGui.QKeySequence.MoveToStartOfBlock),
    move_to_start_of_document=int(QtGui.QKeySequence.MoveToStartOfDocument),
    move_to_start_of_line=int(QtGui.QKeySequence.MoveToStartOfLine),
    new=int(QtGui.QKeySequence.New),
    next_child=int(QtGui.QKeySequence.NextChild),
    open=int(QtGui.QKeySequence.Open),
    paste=int(QtGui.QKeySequence.Paste),
    preferences=int(QtGui.QKeySequence.Preferences),
    previous_child=int(QtGui.QKeySequence.PreviousChild),
    print=int(QtGui.QKeySequence.Print),
    quit=int(QtGui.QKeySequence.Quit),
    redo=int(QtGui.QKeySequence.Redo),
    refresh=int(QtGui.QKeySequence.Refresh),
    replace=int(QtGui.QKeySequence.Replace),
    save_as=int(QtGui.QKeySequence.SaveAs),
    save=int(QtGui.QKeySequence.Save),
    select_all=int(QtGui.QKeySequence.SelectAll),
    deselect=int(QtGui.QKeySequence.Deselect),
    select_end_of_block=int(QtGui.QKeySequence.SelectEndOfBlock),
    select_end_of_document=int(QtGui.QKeySequence.SelectEndOfDocument),
    select_end_of_line=int(QtGui.QKeySequence.SelectEndOfLine),
    select_next_char=int(QtGui.QKeySequence.SelectNextChar),
    select_next_line=int(QtGui.QKeySequence.SelectNextLine),
    select_next_page=int(QtGui.QKeySequence.SelectNextPage),
    select_next_word=int(QtGui.QKeySequence.SelectNextWord),
    select_previous_char=int(QtGui.QKeySequence.SelectPreviousChar),
    select_previous_line=int(QtGui.QKeySequence.SelectPreviousLine),
    select_previous_page=int(QtGui.QKeySequence.SelectPreviousPage),
    select_previous_word=int(QtGui.QKeySequence.SelectPreviousWord),
    select_start_of_block=int(QtGui.QKeySequence.SelectStartOfBlock),
    select_start_of_document=int(QtGui.QKeySequence.SelectStartOfDocument),
    select_start_of_line=int(QtGui.QKeySequence.SelectStartOfLine),
    underline=int(QtGui.QKeySequence.Underline),
    undo=int(QtGui.QKeySequence.Undo),
    unknown_key=int(QtGui.QKeySequence.UnknownKey),
    whats_this=int(QtGui.QKeySequence.WhatsThis),
    zoom_in=int(QtGui.QKeySequence.ZoomIn),
    zoom_out=int(QtGui.QKeySequence.ZoomOut),
    full_screen=int(QtGui.QKeySequence.FullScreen),
    cancel=int(QtGui.QKeySequence.Cancel),
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
        return self.__class__, (self.toString(),)

    def get_matches(self, seq: Union[QtGui.QKeySequence, str]):
        if isinstance(seq, str):
            seq = KeySequence(seq)
        return SEQUENCE_MATCHES.inverse[self.matches(seq)]

    @classmethod
    def to_shortcut_str(cls, key, mod=0):
        for k, v in MODS.items():
            if mod & k:
                key += v
        return str(cls(key))


if __name__ == "__main__":
    seq = KeySequence("select_all")
