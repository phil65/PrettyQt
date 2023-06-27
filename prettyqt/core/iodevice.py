from __future__ import annotations

import contextlib
from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


mod = core.QIODeviceBase  # type: ignore

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

OPEN_MODES: Literal[OpenModeStr, mod.OpenModeFlag] = bidict(
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


class IODeviceMixin(core.ObjectMixin):
    def __len__(self):
        return self.size()

    @contextlib.contextmanager
    def open_file(self, mode: OpenModeStr | mod.OpenModeFlag):
        self.open(OPEN_MODES.get_enum_value(mode))
        yield self
        self.close()

    def get_open_mode(self) -> OpenModeStr:
        return OPEN_MODES.inverse[self.openMode()]


class IODevice(IODeviceMixin, core.QIODevice):
    pass
