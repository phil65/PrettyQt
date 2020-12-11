import contextlib

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict


OPEN_MODES = bidict(
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

QtCore.QIODevice.__bases__ = (core.Object,)


class IODevice(QtCore.QIODevice):
    @contextlib.contextmanager
    def open_file(self, mode: str):
        if mode in OPEN_MODES:
            mode = OPEN_MODES[mode]
        self.open(mode)
        yield self
        self.close()

    def get_open_mode(self) -> str:
        return OPEN_MODES.inverse[self.openMode()]
