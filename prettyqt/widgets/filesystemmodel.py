from __future__ import annotations

from collections.abc import Sequence
import os
import pathlib
from typing import Literal

from prettyqt import constants, core, qt, widgets
from prettyqt.utils import bidict, datatypes


OptionStr = Literal["dont_watch_changes", "dont_resolve_symlinks", "no_custom_icons"]

OPTIONS: bidict[OptionStr, widgets.QFileSystemModel.Option] = bidict(
    dont_watch_changes=widgets.QFileSystemModel.Option.DontWatchForChanges,
    dont_resolve_symlinks=widgets.QFileSystemModel.Option.DontResolveSymlinks,
    no_custom_icons=widgets.QFileSystemModel.Option.DontUseCustomDirectoryIcons,
)


class FileSystemModelMixin:
    """Class to populate a filesystem treeview."""

    DATA_ROLE = constants.USER_ROLE + 33  # type: ignore
    content_type = "files"

    def __init__(self, *args, read_only: bool = False, **kwargs):
        super().__init__(*args, read_only=read_only, **kwargs)
        self.use_custom_icons(False)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role == constants.USER_ROLE:
            path = index.data(self.Roles.FilePathRole)
            return pathlib.Path(path)
        return super().data(index, role)

    def parent(self, *args):
        # workaround: PyQt6 QFileSystemModel.parent() missing
        if not args and qt.API == "pyqt6":
            return core.QAbstractItemModel.parent(self)
        return super().parent(*args)

    def get_file_info(self, index: core.ModelIndex) -> core.FileInfo:
        return core.FileInfo(self.fileInfo(index))

    def get_file_path(self, index: core.ModelIndex) -> pathlib.Path:
        return pathlib.Path(self.filePath(index))

    def resolve_sym_links(self, resolve: bool):
        self.setResolveSymlinks(resolve)

    def watch_for_changes(self, watch: bool):
        self.setOption(OPTIONS["dont_watch_changes"], not watch)

    def use_custom_icons(self, use: bool):
        self.setOption(OPTIONS["no_custom_icons"], not use)

    def set_root_path(self, path: datatypes.PathType) -> core.ModelIndex:
        match path:
            case "root":
                path = core.Dir.rootPath()
            case "home":
                path = core.Dir.homePath()
            case "temp":
                path = core.Dir.tempPath()
            case "current":
                path = core.Dir.currentPath()
            case _:
                path = os.fspath(path)
        return self.setRootPath(path)

    def set_name_filters(self, filters, hide: bool = False):
        self.setNameFilters(filters)
        self.setNameFilterDisables(not hide)

    def set_filter(self, filter_mode: core.dir.FilterStr | core.QDir.Filter):
        self.setFilter(core.dir.FILTERS.get_enum_value(filter_mode))

    def get_paths(self, indexes: Sequence[core.ModelIndex]) -> list[pathlib.Path]:
        paths = [i.data(self.Roles.FilePathRole) for i in indexes]
        if not paths:
            return []
        if not paths[0]:
            paths = [
                folder / filename
                for folder in paths
                for filename in folder.iterdir()
                if (folder / filename).is_file()
            ]
        return paths

    def get_permissions(
        self, index: core.ModelIndex
    ) -> list[core.filedevice.PermissionStr]:
        return core.filedevice.PERMISSIONS.get_list(self.permissions(index))


class FileSystemModel(
    FileSystemModelMixin, core.AbstractItemModelMixin, widgets.QFileSystemModel
):
    pass


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    app.load_language("de")
    model = FileSystemModel()
    model.set_root_path("root")
    tree = widgets.TreeView()
    tree.set_model(model)
    tree.show()
    app.exec()
