from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING, Literal, Self

from prettyqt import core
from prettyqt.utils import bidict, get_repr


if TYPE_CHECKING:
    from collections.abc import Iterable

    from prettyqt.utils import datatypes


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

FILTERS: bidict[FilterStr, core.QDir.Filter] = bidict(
    none=core.QDir.Filter.NoFilter,
    dirs=core.QDir.Filter.Dirs,
    all_dirs=core.QDir.Filter.AllDirs,
    files=core.QDir.Filter.Files,
    drives=core.QDir.Filter.Drives,
    no_sym_links=core.QDir.Filter.NoSymLinks,
    no_dot_and_dotdot=core.QDir.Filter.NoDotAndDotDot,
    no_dot=core.QDir.Filter.NoDot,
    no_dotdot=core.QDir.Filter.NoDotDot,
    all_entries=core.QDir.Filter.AllEntries,
    readable=core.QDir.Filter.Readable,
    writable=core.QDir.Filter.Writable,
    executable=core.QDir.Filter.Executable,
    modified=core.QDir.Filter.Modified,
    hidden=core.QDir.Filter.Hidden,
    system=core.QDir.Filter.System,
    case_sensitive=core.QDir.Filter.CaseSensitive,
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

SORT_FLAG: bidict[SortFlagStr, core.QDir.SortFlag] = bidict(
    name=core.QDir.SortFlag.Name,
    time=core.QDir.SortFlag.Time,
    size=core.QDir.SortFlag.Size,
    type=core.QDir.SortFlag.Type,
    unsorted=core.QDir.SortFlag.Unsorted,
    no_sort=core.QDir.SortFlag.NoSort,
    dirs_first=core.QDir.SortFlag.DirsFirst,
    dirs_last=core.QDir.SortFlag.DirsLast,
    reversed=core.QDir.SortFlag.Reversed,
    ignore_case=core.QDir.SortFlag.IgnoreCase,
    locale_aware=core.QDir.SortFlag.LocaleAware,
)


class Dir(core.QDir):
    """Access to directory structures and their contents."""

    def __getattr__(self, attr: str):
        return getattr(self.to_path(), attr)

    def __repr__(self):
        return get_repr(self, self.absolutePath())

    def __str__(self):
        return self.absolutePath()

    def __reduce__(self):
        return type(self), (self.absolutePath(),)

    def __truediv__(self, other: datatypes.PathType) -> pathlib.Path:
        return self.to_path() / os.fspath(other)

    def __fspath__(self) -> str:
        return self.absolutePath()

    def __bool__(self):
        return self.exists()

    def __abs__(self) -> str:
        return self.absolutePath()

    @property
    def _absolutePath(self) -> str:
        return self.absolutePath()

    __match_args__ = ("_absolutePath",)

    def to_path(self) -> pathlib.Path:
        return pathlib.Path(self.absolutePath())

    def set_filter(self, *filters: FilterStr):
        flags = FILTERS.merge_flags(filters)
        self.setFilter(flags)

    def get_filter(self) -> list[FilterStr]:
        return FILTERS.get_list(self.filter())

    def get_entry_info_list(
        self, sort_mode: SortFlagStr = "no_sort", filters: FilterStr = "none"
    ) -> list[core.FileInfo]:
        return [
            core.FileInfo(i)
            for i in self.entryInfoList(
                sort=SORT_FLAG[sort_mode],
                filters=self.Filter.AllEntries | FILTERS[filters],
            )
        ]

    def get_entry_list(
        self, sort_mode: SortFlagStr = "no_sort", filters: FilterStr = "none"
    ) -> list[pathlib.Path]:
        return [
            pathlib.Path(i)
            for i in self.entryList(sort=SORT_FLAG[sort_mode], filters=FILTERS[filters])
        ]

    @classmethod
    def get_current(cls) -> Self:
        return cls(cls.current())

    @classmethod
    def get_home(cls) -> Self:
        return cls(cls.home())

    @classmethod
    def get_current_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.currentPath())

    @classmethod
    def get_home_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.homePath())

    @classmethod
    def get_temp_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.tempPath())

    @classmethod
    def get_drives(cls) -> list[core.FileInfo]:
        return [core.FileInfo(i) for i in cls.drives()]

    @classmethod
    def add_search_path(cls, prefix: str, path: datatypes.PathType):
        cls.addSearchPath(prefix, os.fspath(path))

    @classmethod
    def set_search_paths(cls, prefix: str, paths: Iterable[datatypes.PathType]):
        cls.setSearchPaths(prefix, [os.fspath(p) for p in paths])


if __name__ == "__main__":
    path = Dir.get_temp_path()
