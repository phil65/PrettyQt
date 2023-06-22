# type: ignore
# not available in PySide2

from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


LoadHintStr = Literal[
    "resolve_all_symbols",
    "export_external_symbols",
    "load_archive_member",
    "prevent_unload",
    "deep_bind",
]

LOAD_HINTS: bidict[LoadHintStr, QtCore.QLibrary.LoadHint] = bidict(
    resolve_all_symbols=QtCore.QLibrary.LoadHint.ResolveAllSymbolsHint,
    export_external_symbols=QtCore.QLibrary.LoadHint.ExportExternalSymbolsHint,
    load_archive_member=QtCore.QLibrary.LoadHint.LoadArchiveMemberHint,
    prevent_unload=QtCore.QLibrary.LoadHint.PreventUnloadHint,
    deep_bind=QtCore.QLibrary.LoadHint.DeepBindHint,
)


class Library(core.ObjectMixin, QtCore.QLibrary):
    def __bool__(self):
        return self.isLoaded()

    def __repr__(self):
        return get_repr(self, self.fileName())

    def get_load_hints(self) -> list[LoadHintStr]:
        return LOAD_HINTS.get_list(self.loadHints())

    def set_load_hints(self, **kwargs):
        flag = QtCore.QLibrary.LoadHint(0)
        for k, v in kwargs.items():
            if v is True:
                flag |= LOAD_HINTS[k]
        self.setLoadHints(flag)
