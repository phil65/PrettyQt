import pathlib
from typing import List, Literal

from qtpy import QtCore

from prettyqt.utils import InvalidParamError, bidict, helpers


FILTERS = bidict(
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


class Dir(QtCore.QDir):
    def __getattr__(self, attr: str):
        return getattr(self.to_path(), attr)

    def __repr__(self):
        return f"{type(self).__name__}({self.absolutePath()!r})"

    def __str__(self):
        return self.absolutePath()

    def __reduce__(self):
        return self.__class__, (self.absolutePath(),)

    def __truediv__(self, other: str) -> pathlib.Path:
        return self.to_path() / other

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
