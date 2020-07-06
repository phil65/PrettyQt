# -*- coding: utf-8 -*-
"""
"""

import pathlib

from qtpy import QtCore, QtWidgets

from prettyqt import core
from prettyqt.utils import bidict


OPTIONS = bidict(
    dont_watch_changes=QtWidgets.QFileSystemModel.DontWatchForChanges,
    dont_resolve_symlinks=QtWidgets.QFileSystemModel.DontResolveSymlinks,
    no_custom_icons=QtWidgets.QFileSystemModel.DontUseCustomDirectoryIcons,
)

FILTERS = bidict(
    dirs=core.Dir.Dirs,
    all_dirs=core.Dir.AllDirs,
    files=core.Dir.Files,
    drives=core.Dir.Drives,
    no_sym_links=core.Dir.NoSymLinks,
    no_dot_and_dotdot=core.Dir.NoDotAndDotDot,
    no_dot=core.Dir.NoDot,
    no_dotdot=core.Dir.NoDotDot,
    all_entries=core.Dir.AllEntries,
    readable=core.Dir.Readable,
    writable=core.Dir.Writable,
    executable=core.Dir.Executable,
    modified=core.Dir.Modified,
    hidden=core.Dir.Hidden,
    system=core.Dir.System,
    case_sensitive=core.Dir.CaseSensitive,
)

QtWidgets.QFileSystemModel.__bases__ = (core.AbstractItemModel,)


class FileSystemModel(QtWidgets.QFileSystemModel):
    """
    Class to populate a filesystem treeview
    """

    DATA_ROLE = QtCore.Qt.UserRole + 33
    content_type = "files"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setReadOnly(False)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == self.DATA_ROLE:
            path = index.data(self.FilePathRole)
            return pathlib.Path(path)
        return super().data(index, role)

    def yield_child_indexes(self, index):
        if not self.hasChildren(index):
            return None
        path = self.filePath(index)
        flags = self.filter() | QtCore.QDir.NoDotAndDotDot
        for it in core.DirIterator(path, flags):
            yield self.index(it)

    def resolve_sym_links(self, resolve: bool):
        self.setResolveSymlinks(resolve)

    def watch_for_changes(self, watch: bool):
        self.setOption(OPTIONS["dont_watch_changes"], not watch)

    def use_custom_icons(self, use: bool):
        self.setOption(OPTIONS["no_custom_icons"], not use)

    def set_root_path(self, path: str):
        if path == "/":
            path = core.Dir.rootPath()
        self.setRootPath(path)

    def set_name_filters(self, filters, hide=False):
        self.setNameFilters(filters)
        self.setNameFilterDisables(not hide)

    def set_filter(self, filter_mode: str):
        if filter_mode not in FILTERS:
            raise ValueError(f"Invalid value. Valid values: {FILTERS.keys()}")
        self.setFilter(FILTERS[filter_mode])

    def get_paths(self, indexes):
        paths = [i.data(self.DATA_ROLE) for i in indexes]
        if not paths:
            return []
        if paths[0] == "":
            paths = [
                folder / filename
                for folder in paths
                for filename in folder.iterdir()
                if (folder / filename).is_file()
            ]
        return paths
