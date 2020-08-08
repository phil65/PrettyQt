# -*- coding: utf-8 -*-

from qtpy import QtCore, QtGui

from prettyqt.utils import bidict


SEQUENCE_MATCHES = bidict(
    none=QtGui.QKeySequence.NoMatch,
    partial=QtGui.QKeySequence.PartialMatch,
    exact=QtGui.QKeySequence.ExactMatch,
)

MODS = {
    QtCore.Qt.ShiftModifier: QtCore.Qt.SHIFT,
    QtCore.Qt.ControlModifier: QtCore.Qt.CTRL,
    QtCore.Qt.AltModifier: QtCore.Qt.ALT,
    QtCore.Qt.MetaModifier: QtCore.Qt.META,
}


class KeySequence(QtGui.QKeySequence):
    def __str__(self):
        return self.toString()

    def __repr__(self):
        return f"KeySequence({self.toString()!r})"

    def __bool__(self):
        return not self.isEmpty()

    def __reduce__(self):
        return (self.__class__, (self.toString()))

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
