from __future__ import annotations

import os
import pathlib
from typing import List, Literal, Union

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict, helpers


FILTERS = bidict(
    none=QtCore.QDir.NoFilter,
    dirs=QtCore.QDir.Dirs,
    all_dirs=QtCore.QDir.AllDirs,
    files=QtCore.QDir.Files,
    drives=QtCore.QDir.Drives,
    no_sym_links=QtCore.QDir.NoSymLinks,
    no_dot_and_dotdot=QtCore.QDir.NoDotAndDotDot,
    no_dot=QtCore.QDir.NoDot,
    no_dotdot=QtCore.QDir.NoDotDot,
    all_entries=QtCore.QDir.AllEntries,
    readable=QtCore.QDir.Readable,
    writable=QtCore.QDir.Writable,
    executable=QtCore.QDir.Executable,
    modified=QtCore.QDir.Modified,
    hidden=QtCore.QDir.Hidden,
    system=QtCore.QDir.System,
    case_sensitive=QtCore.QDir.CaseSensitive,
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
    name=QtCore.QDir.Name,
    time=QtCore.QDir.Time,
    size=QtCore.QDir.Size,
    type=QtCore.QDir.Type,
    unsorted=QtCore.QDir.Unsorted,
    no_sort=QtCore.QDir.NoSort,
    dirs_first=QtCore.QDir.DirsFirst,
    dirs_last=QtCore.QDir.DirsLast,
    reversed=QtCore.QDir.Reversed,
    ignore_case=QtCore.QDir.IgnoreCase,
    locale_aware=QtCore.QDir.LocaleAware,
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

    def __truediv__(self, other: os.PathLike) -> pathlib.Path:
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

    def get_filter(self) -> List[FilterStr]:
        return [k for k, v in FILTERS.items() if v & self.filter()]

    def get_entry_info_list(
        self, sort_mode: SortFlagStr = "no_sort", filters: FilterStr = "none"
    ) -> List[core.FileInfo]:
        return [
            core.FileInfo(i)
            for i in self.entryInfoList(SORT_FLAG[sort_mode], FILTERS[filters])
        ]

    def get_entry_list(
        self, sort_mode: SortFlagStr = "no_sort", filters: FilterStr = "none"
    ) -> List[pathlib.Path]:
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
    def get_drives(cls) -> List[core.FileInfo]:
        return [core.FileInfo(i) for i in cls.drives()]

    @classmethod
    def add_search_path(cls, prefix: str, path: Union[str, os.PathLike]):
        cls.addSearchPath(prefix, os.fspath(path))

    @classmethod
    def set_search_paths(cls, prefix: str, paths: List[Union[str, os.PathLike]]):
        cls.setSearchPaths(prefix, [os.fspath(p) for p in paths])
