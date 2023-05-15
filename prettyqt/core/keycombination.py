from __future__ import annotations

import functools
from operator import or_

from prettyqt import constants
from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr, serializemixin


Mod = QtCore.Qt.KeyboardModifier
Key = QtCore.Qt.Key

MODIFIERS = bidict(
    {
        "None": Mod.NoModifier,
        "Shift": Mod.ShiftModifier,
        "Ctrl": Mod.ControlModifier,
        "Alt": Mod.AltModifier,
        "Meta": Mod.MetaModifier,
        "Ctrl+Shift": Mod.ControlModifier | Mod.ShiftModifier,
        "Ctrl+Alt": Mod.ControlModifier | Mod.AltModifier,
        "Alt+Shift": Mod.AltModifier | Mod.ShiftModifier,
    }
)

MODIFIER_KEYS = frozenset({Key.Key_Shift, Key.Key_Control, Key.Key_Meta, Key.Key_Alt})
ARROW_KEYS = frozenset({Key.Key_Up, Key.Key_Down, Key.Key_Left, Key.Key_Right})
FUNC_ARROW_KEYS = frozenset({Key.Key_Home, Key.Key_End, Key.Key_PageUp, Key.Key_PageDown})

_SYMBOLS = {
    "Esc": "Escape",
    "!": "Exclam",
    '"': "QuoteDbl",
    "#": "NumberSign",
    "$": "Dollar",
    "%": "Percent",
    "&": "Ampersand",
    "'": "Apostrophe",
    "(": "ParenLeft",
    ")": "ParenRight",
    "*": "Asterisk",
    "+": "Plus",
    ",": "Comma",
    "-": "Minus",
    ".": "Period",
    "/": "Slash",
    ":": "Colon",
    ";": "Semicolon",
    "<": "Less",
    "=": "Equal",
    ">": "Greater",
    "?": "Question",
    "@": "At",
    "[": "BracketLeft",
    "\\": "Backslash",
    "]": "BracketRight",
    "^": "AsciiCircum",
    "_": "Underscore",
    "`": "QuoteLeft",
    "{": "BraceLeft",
    "|": "Bar",
    "}": "BraceRight",
    "~": "AsciiTilde",
}


class Keys:
    """Key extension."""

    No = Key(-1)
    Any = Key(-2)

    ALPHA = Key(913)  # α
    OMEGA = Key(937)  # ω

    CYR_A = Key(1040)  # а
    CYR_YA = Key(1071)  # я


class KeyCombination(serializemixin.SerializeMixin, QtCore.QKeyCombination):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            if args[0] in MODIFIERS.inverse.values():
                mods = args[0].split("+")
                qtmod = functools.reduce(or_, [MODIFIERS[m] for m in mods])
                super().__init__(qtmod, Keys.No)
                return
            *mods, btn = args[0].split("+")

            # get modifiler
            qtmod = (
                functools.reduce(or_, [MODIFIERS[m] for m in mods])
                if mods
                else Mod.NoModifier
            )
            # get button
            if btn in _SYMBOLS:
                btn = _SYMBOLS[btn]

            qtkey = getattr(Key, f"Key_{btn}") if btn != "{}" else Keys.Any
            super().__init__(qtmod, qtkey)
        elif len(args) == 1 and isinstance(args[0], QtCore.QEvent):
            modifier = args[0].modifiers()
            modifier ^= Mod.KeypadModifier
            key = args[0].key()
            if key in MODIFIER_KEYS:  # modifier only
                key = Keys.No
            super().__init__(key, modifier)
        else:
            super().__init__(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, str | Key):
            other = KeyCombination(other)
        return super().__eq__(other)

    def __repr__(self):
        return get_repr(self, self.key(), self.keyboardModifiers())

    def is_typing(self) -> bool:
        """True if key is a letter or number."""
        mod_ok = self.keyboardModifiers() in (Mod.NoModifier, Mod.ShiftModifier)
        key = self.key()
        key_ok = (
            Key.Key_Exclam <= key <= Key.Key_ydiaeresis
            or Keys.ALPHA <= key <= Keys.OMEGA
            or Keys.CYR_A <= key <= Keys.CYR_YA
        )
        return mod_ok and key_ok

    def is_moving(self) -> bool:
        """True if arrows are pushed."""
        return self.key() in ARROW_KEYS

    def is_moving_func(self) -> bool:
        """True if function arrows are pushed."""
        return self.key() in FUNC_ARROW_KEYS

    def has_ctrl(self) -> bool:
        """True if Ctrl is pressed."""
        return bool(self.keyboardModifiers() & Mod.ControlModifier)

    def has_shift(self) -> bool:
        """True if Shift is pressed."""
        return bool(self.keyboardModifiers() & Mod.ShiftModifier)

    def has_alt(self) -> bool:
        """True if Alt is pressed."""
        return bool(self.keyboardModifiers() & Mod.AltModifier)

    def has_key(self) -> bool:
        """True if non-modifier key is pressed."""
        return self.key() != Keys.No

    def get_key(self) -> constants.KeyStr:
        return constants.KEY.inverse[self.key()]

    def get_modifiers(self) -> list[constants.KeyboardmodifierStr]:
        return constants.KEYBOARD_MODIFIERS.get_list(self.keyboardModifiers())


if __name__ == "__main__":
    seq = KeyCombination(Key(1))
    print(seq)
