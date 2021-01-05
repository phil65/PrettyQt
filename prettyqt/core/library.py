# type: ignore
# not available in PySide2

from __future__ import annotations

from typing import List, Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


LOAD_HINTS = bidict(
    resolve_all_symbols=QtCore.QLibrary.ResolveAllSymbolsHint,
    export_external_symbols=QtCore.QLibrary.ExportExternalSymbolsHint,
    load_archive_member=QtCore.QLibrary.LoadArchiveMemberHint,
    prevent_unload=QtCore.QLibrary.PreventUnloadHint,
    deep_bind=QtCore.QLibrary.DeepBindHint,
)

LoadHintStr = Literal[
    "resolve_all_symbols",
    "export_external_symbols",
    "load_archive_member",
    "prevent_unload",
    "deep_bind",
]

QtCore.QLibrary.__bases__ = (core.Object,)


class Library(QtCore.QLibrary):
    def __bool__(self):
        return self.isLoaded()

    def __repr__(self):
        return f"{type(self).__name__}({self.fileName()!r})"

    def get_load_hints(self) -> List[LoadHintStr]:
        return [k for k, v in LOAD_HINTS.items() if v & self.loadHints()]

    def set_load_hints(self, **kwargs):
        flag = QtCore.QLibrary.LoadHint(0)
        for k, v in kwargs.items():
            if v is True:
                flag |= LOAD_HINTS[k]
        self.setLoadHints(flag)
