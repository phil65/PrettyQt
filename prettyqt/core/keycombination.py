from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtCore


class KeyCombination(QtCore.QKeyCombination):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str) and args[0] in constants.KEY:
            super().__init__(constants.KEY[args[0]], **kwargs)
        else:
            super().__init__(*args, **kwargs)

    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return ba.data()

    def get_key(self) -> constants.KeyStr:
        return constants.KEY.inverse[self.key()]

    def get_modifiers(self) -> list[constants.KeyboardmodifierStr]:
        return [
            k for k, v in constants.KEYBOARD_MODIFIERS.items() if v & self.modifiers()
        ]


if __name__ == "__main__":
    seq = KeyCombination("a")
