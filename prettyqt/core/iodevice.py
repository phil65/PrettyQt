import contextlib
from typing import Literal

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import mappers


OPEN_MODES = mappers.FlagMap(
    QtCore.QIODevice.OpenModeFlag,
    not_open=QtCore.QIODevice.NotOpen,
    read_only=QtCore.QIODevice.ReadOnly,
    write_only=QtCore.QIODevice.WriteOnly,
    read_write=QtCore.QIODevice.ReadWrite,
    append=QtCore.QIODevice.Append,
    truncate=QtCore.QIODevice.Truncate,
    text=QtCore.QIODevice.Text,
    unbuffered=QtCore.QIODevice.Unbuffered,
    new_only=QtCore.QIODevice.NewOnly,
    existing_only=QtCore.QIODevice.ExistingOnly,
)

OpenModeStr = Literal[
    "not_open",
    "read_only",
    "write_only",
    "read_write",
    "append",
    "truncate",
    "text",
    "unbuffered",
    "new_only",
    "existing_only",
]

QtCore.QIODevice.__bases__ = (core.Object,)


class IODevice(QtCore.QIODevice):
    @contextlib.contextmanager
    def open_file(self, mode: OpenModeStr):
        if mode in OPEN_MODES:
            mode = OPEN_MODES[mode]
        self.open(mode)
        yield self
        self.close()

    def get_open_mode(self) -> OpenModeStr:
        return OPEN_MODES.inverse[self.openMode()]
