from __future__ import annotations

import contextlib
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, mappers


if core.VersionNumber.get_qt_version() >= (6, 0, 0):
    mod = QtCore.QIODeviceBase  # type: ignore
    base = (core.Object, QtCore.QIODeviceBase)  # type: ignore
else:
    mod = QtCore.QIODevice  # type: ignore
    base = (core.Object,)  # type: ignore

OPEN_MODES = mappers.FlagMap(
    mod.OpenModeFlag,
    not_open=mod.OpenModeFlag.NotOpen,
    read_only=mod.OpenModeFlag.ReadOnly,
    write_only=mod.OpenModeFlag.WriteOnly,
    read_write=mod.OpenModeFlag.ReadWrite,
    append=mod.OpenModeFlag.Append,
    truncate=mod.OpenModeFlag.Truncate,
    text=mod.OpenModeFlag.Text,
    unbuffered=mod.OpenModeFlag.Unbuffered,
    new_only=mod.OpenModeFlag.NewOnly,
    existing_only=mod.OpenModeFlag.ExistingOnly,
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

QtCore.QIODevice.__bases__ = base


class IODevice(QtCore.QIODevice):
    def __len__(self):
        return self.size()

    @contextlib.contextmanager
    def open_file(self, mode: OpenModeStr):
        if mode not in OPEN_MODES:
            raise InvalidParamError(mode, OPEN_MODES)
        self.open(OPEN_MODES[mode])
        yield self
        self.close()

    def get_open_mode(self) -> OpenModeStr:
        return OPEN_MODES.inverse[self.openMode()]
