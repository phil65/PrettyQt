import pathlib
from typing import Iterator, List, Sequence, Union

from qtpy import QtCore, QtWidgets

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


if core.VersionNumber.get_qt_version() >= (5, 14, 0):
    OPTIONS = bidict(
        dont_watch_changes=QtWidgets.QFileSystemModel.DontWatchForChanges,
        dont_resolve_symlinks=QtWidgets.QFileSystemModel.DontResolveSymlinks,
        no_custom_icons=QtWidgets.QFileSystemModel.DontUseCustomDirectoryIcons,
    )

QtWidgets.QFileSystemModel.__bases__ = (core.AbstractItemModel,)


class FileSystemModel(QtWidgets.QFileSystemModel):
    """Class to populate a filesystem treeview."""

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

    def yield_child_indexes(
        self, index: QtCore.QModelIndex
    ) -> Iterator[QtCore.QModelIndex]:
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

    def set_root_path(self, path: Union[str, pathlib.Path]):
        path = str(path)
        if path in ["/", "root"]:
            path = core.Dir.rootPath()
        elif path == "home":
            path = core.Dir.homePath()
        elif path == "temp":
            path = core.Dir.tempPath()
        elif path == "current":
            path = core.Dir.currentPath()
        self.setRootPath(path)

    def set_name_filters(self, filters, hide: bool = False):
        self.setNameFilters(filters)
        self.setNameFilterDisables(not hide)

    def set_filter(self, filter_mode: core.dir.FilterStr):
        if filter_mode not in core.dir.FILTERS:
            raise InvalidParamError(filter_mode, core.dir.FILTERS)
        self.setFilter(core.dir.FILTERS[filter_mode])

    def get_paths(self, indexes: Sequence[QtCore.QModelIndex]) -> List[pathlib.Path]:
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
