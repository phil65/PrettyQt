from __future__ import annotations

import os
import pathlib
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict, helpers, types


FILTERS = bidict(
    none=QtCore.QDir.Filter.NoFilter,
    dirs=QtCore.QDir.Filter.Dirs,
    all_dirs=QtCore.QDir.Filter.AllDirs,
    files=QtCore.QDir.Filter.Files,
    drives=QtCore.QDir.Filter.Drives,
    no_sym_links=QtCore.QDir.Filter.NoSymLinks,
    no_dot_and_dotdot=QtCore.QDir.Filter.NoDotAndDotDot,
    no_dot=QtCore.QDir.Filter.NoDot,
    no_dotdot=QtCore.QDir.Filter.NoDotDot,
    all_entries=QtCore.QDir.Filter.AllEntries,
    readable=QtCore.QDir.Filter.Readable,
    writable=QtCore.QDir.Filter.Writable,
    executable=QtCore.QDir.Filter.Executable,
    modified=QtCore.QDir.Filter.Modified,
    hidden=QtCore.QDir.Filter.Hidden,
    system=QtCore.QDir.Filter.System,
    case_sensitive=QtCore.QDir.Filter.CaseSensitive,
)

FilterStr = Literal[
    "none",
    "dirs",
    "all_dirs",
    "files",
    "drives",
    "no_sym_links",
    "no_dot_and_dotdot",
    "no_dot",
    "no_dotdot",
    "all_entries",
    "readable",
    "writable",
    "executable",
    "modified",
    "hidden",
    "system",
    "case_sensitive",
]

SORT_FLAG = bidict(
    name=QtCore.QDir.SortFlag.Name,
    time=QtCore.QDir.SortFlag.Time,
    size=QtCore.QDir.SortFlag.Size,
    type=QtCore.QDir.SortFlag.Type,
    unsorted=QtCore.QDir.SortFlag.Unsorted,
    no_sort=QtCore.QDir.SortFlag.NoSort,
    dirs_first=QtCore.QDir.SortFlag.DirsFirst,
    dirs_last=QtCore.QDir.SortFlag.DirsLast,
    reversed=QtCore.QDir.SortFlag.Reversed,
    ignore_case=QtCore.QDir.SortFlag.IgnoreCase,
    locale_aware=QtCore.QDir.SortFlag.LocaleAware,
)

SortFlagStr = Literal[
    "name",
    "time",
    "size",
    "type",
    "unsorted",
    "no_sort",
    "dirs_first",
    "dirs_last",
    "reversed",
    "ignore_case",
    "locale_aware",
]


class Dir(QtCore.QDir):
    def __getattr__(self, attr: str):
        return getattr(self.to_path(), attr)

    def __repr__(self):
        return f"{type(self).__name__}({self.absolutePath()!r})"

    def __str__(self):
        return self.absolutePath()

    def __reduce__(self):
        return type(self), (self.absolutePath(),)

    def __truediv__(self, other: types.PathType) -> pathlib.Path:
        return self.to_path() / os.fspath(other)

    def __fspath__(self) -> str:
        return self.absolutePath()

    def __bool__(self):
        return self.exists()

    def __abs__(self) -> str:
        return self.absolutePath()

    def to_path(self) -> pathlib.Path:
        return pathlib.Path(self.absolutePath())

    def set_filter(self, *filters: FilterStr):
        for item in filters:
            if item not in FILTERS:
                raise InvalidParamError(item, FILTERS)
        flags = helpers.merge_flags(filters, FILTERS)
        self.setFilter(flags)

    def get_filter(self) -> list[FilterStr]:
        return [k for k, v in FILTERS.items() if v & self.filter()]

    def get_entry_info_list(
        self, sort_mode: SortFlagStr = "no_sort", filters: FilterStr = "none"
    ) -> list[core.FileInfo]:
        return [
            core.FileInfo(i)
            for i in self.entryInfoList(SORT_FLAG[sort_mode], FILTERS[filters])
        ]

    def get_entry_list(
        self, sort_mode: SortFlagStr = "no_sort", filters: FilterStr = "none"
    ) -> list[pathlib.Path]:
        return [
            pathlib.Path(i)
            for i in self.entryList(SORT_FLAG[sort_mode], FILTERS[filters])
        ]

    @classmethod
    def get_current(cls) -> Dir:
        return cls(cls.current())

    @classmethod
    def get_home(cls) -> Dir:
        return cls(cls.home())

    @classmethod
    def get_current_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.currentPath())

    @classmethod
    def get_home_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.homePath())

    @classmethod
    def get_drives(cls) -> list[core.FileInfo]:
        return [core.FileInfo(i) for i in cls.drives()]

    @classmethod
    def add_search_path(cls, prefix: str, path: types.PathType):
        cls.addSearchPath(prefix, os.fspath(path))

    @classmethod
    def set_search_paths(cls, prefix: str, paths: list[types.PathType]):
        cls.setSearchPaths(prefix, [os.fspath(p) for p in paths])
