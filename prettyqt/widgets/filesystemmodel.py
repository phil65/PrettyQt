from __future__ import annotations

from collections.abc import Iterator, Sequence
import os
import pathlib

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


OPTIONS = bidict(
    dont_watch_changes=QtWidgets.QFileSystemModel.Option.DontWatchForChanges,
    dont_resolve_symlinks=QtWidgets.QFileSystemModel.Option.DontResolveSymlinks,
    no_custom_icons=QtWidgets.QFileSystemModel.Option.DontUseCustomDirectoryIcons,
)

QtWidgets.QFileSystemModel.__bases__ = (core.AbstractItemModel,)


class FileSystemModel(QtWidgets.QFileSystemModel):
    """Class to populate a filesystem treeview."""

    DATA_ROLE = constants.USER_ROLE + 33  # type: ignore
    content_type = "files"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setReadOnly(False)

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role == self.DATA_ROLE:
            path = index.data(self.Roles.FilePathRole)
            return pathlib.Path(path)
        return super().data(index, role)

    def get_file_info(self, index: QtCore.QModelIndex) -> core.FileInfo:
        return core.FileInfo(self.fileInfo(index))

    def get_file_path(self, index: QtCore.QModelIndex) -> pathlib.Path:
        return pathlib.Path(self.filePath(index))

    def yield_child_indexes(
        self, index: QtCore.QModelIndex
    ) -> Iterator[QtCore.QModelIndex]:
        if not self.hasChildren(index):
            return
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

    def set_root_path(self, path: types.PathType) -> QtCore.QModelIndex:
        path = os.fspath(path)
        if path in ["/", "root"]:
            path = core.Dir.rootPath()
        elif path == "home":
            path = core.Dir.homePath()
        elif path == "temp":
            path = core.Dir.tempPath()
        elif path == "current":
            path = core.Dir.currentPath()
        return self.setRootPath(path)

    def set_name_filters(self, filters, hide: bool = False):
        self.setNameFilters(filters)
        self.setNameFilterDisables(not hide)

    def set_filter(self, filter_mode: core.dir.FilterStr):
        if filter_mode not in core.dir.FILTERS:
            raise InvalidParamError(filter_mode, core.dir.FILTERS)
        self.setFilter(core.dir.FILTERS[filter_mode])

    def get_paths(self, indexes: Sequence[QtCore.QModelIndex]) -> list[pathlib.Path]:
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


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    app.load_language("de")
    model = FileSystemModel()
    model.set_root_path("root")
    tree = widgets.TreeView()
    tree.set_model(model)
    tree.show()
    app.main_loop()
