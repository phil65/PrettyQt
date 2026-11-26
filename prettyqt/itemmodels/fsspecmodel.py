"""Tree model for any filesystem supported by fsspec, with a QFileSystemModel-like API."""

import contextlib
import datetime as dt
import enum
import fnmatch
import json
import logging
import os
from typing import TYPE_CHECKING, Any, ClassVar

import fsspec

from prettyqt import constants, core, gui, itemmodels, widgets


if TYPE_CHECKING:
    from collections.abc import Iterable

    from upath import UPath

    from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)

# Mime type for drag & drop inside the model (json list of paths).
PATHS_MIME_TYPE = "application/x-fsspec-paths"

Filter = core.QDir.Filter
# Like QFileSystemModel default, but hidden files are shown.
DEFAULT_FILTER = (
    Filter.AllEntries | Filter.NoDotAndDotDot | Filter.AllDirs | Filter.Hidden
)


def _to_datetime(value: Any) -> dt.datetime | None:
    """Convert the timestamps of the different fsspec implementations."""
    match value:
        case dt.datetime():
            return value
        case bool() | None:
            return None
        case int() | float():
            return dt.datetime.fromtimestamp(value)
        case str():
            with contextlib.suppress(ValueError):
                return dt.datetime.fromisoformat(value)
    return None


def _get_filesystem(protocol: str, **storage_options: Any) -> fsspec.AbstractFileSystem:
    """Instantiate filesystem for given protocol.

    Uses upathtools (if installed) to support its additional protocols.
    """
    try:
        from upathtools import core as upathtools_core
    except ImportError:
        return fsspec.filesystem(protocol, **storage_options)
    return upathtools_core.filesystem(protocol, **storage_options)


class FsSpecCompleter(widgets.Completer):
    def pathFromIndex(self, index):
        return index.data(self.model().Roles.FilePathRole)

    def splitPath(self, path: str):
        return path.split(self.model().fs.sep)


_icon_provider = widgets.FileIconProvider()


class FsSpecColumnItem(itemmodels.ColumnItem):
    identifier: str = ""
    model: FSSpecTreeModel

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        name = item.obj["name"]
        match role:
            case FSSpecTreeModel.Roles.FilePathRole:
                return name
            case FSSpecTreeModel.Roles.FileNameRole:
                return self.model.get_file_name(name)
            case FSSpecTreeModel.Roles.FilePermissions:
                return self.model.get_permission_flags(item.obj)
            case FSSpecTreeModel.Roles.ProtocolPathRole:
                return self.model.get_protocol_path(name)
        return None


class NameColumn(FsSpecColumnItem):
    identifier = "name"
    name = "Name"
    doc = "File name"
    editable = True

    def get_flags(self, tree_item):
        flags = super().get_flags(tree_item)
        if self.model.isReadOnly() or tree_item is self.model.inspected_item:
            flags &= ~constants.IS_EDITABLE
        return flags

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                return self.model.get_file_name(item.obj["name"])
            case constants.DECORATION_ROLE:
                return self.model.get_icon(item.obj)
            case _:
                return super().get_data(item, role)

    def set_data(self, item, value, role):
        match role:
            case constants.EDIT_ROLE:
                return self.model.rename_item(item, str(value))
        return False


class PathColumn(FsSpecColumnItem):
    identifier = "path"
    name = "Path"
    doc = "File path"

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj["name"] or ""
            case _:
                return super().get_data(item, role)


class SizeColumn(FsSpecColumnItem):
    identifier = "size"
    name = "Size"
    doc = "File size."
    precision = 2
    fmt: core._locale.DataSizeFormatStr = "iec"

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                size = item.obj.get("size") or 0
                if size > 0 and not self.model.is_dir_info(item.obj):
                    return core.Locale().get_formatted_data_size(
                        size, precision=self.precision, fmt=self.fmt
                    )
                return ""
            case constants.SORT_ROLE:
                return item.obj.get("size") or 0
            case _:
                return super().get_data(item, role)


class TypeColumn(FsSpecColumnItem):
    identifier = "type"
    name = "Type"
    doc = "Type of given path."

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj.get("type") or ""
            case _:
                return super().get_data(item, role)


class _DateColumn(FsSpecColumnItem):
    display_format = "%m/%d/%Y, %H:%M:%S"

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                date = _to_datetime(item.obj.get(self.identifier))
                return "" if date is None else date.strftime(self.display_format)
            case constants.USER_ROLE | constants.SORT_ROLE:
                return _to_datetime(item.obj.get(self.identifier))
            case _:
                return super().get_data(item, role)


class CreatedColumn(_DateColumn):
    identifier = "created"
    name = "Created"
    doc = "Creation date of file."


class ModifiedColumn(_DateColumn):
    identifier = "mtime"
    name = "Modified"
    doc = "Modification date of file."


class PermissionsColumn(FsSpecColumnItem):
    identifier = "mode"
    name = "Permissions"
    doc = "File Permissions"

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                if (mode := item.obj.get("mode")) is not None:
                    return oct(int(mode))[-4:]
                return ""
            case _:
                return super().get_data(item, role)


class IsLinkColumn(FsSpecColumnItem):
    identifier = "is_link"
    name = "Is link"
    doc = "Whether file is a symbolic link."

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(bool(item.obj.get("islink")))
            case _:
                return super().get_data(item, role)


class ShaColumn(FsSpecColumnItem):
    identifier = "sha"
    name = "SHA"
    doc = "Hash value."

    def get_data(self, item: FSSpecTreeModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj.get("sha") or ""
            case _:
                return super().get_data(item, role)


FsSpecProtocolStr = str


class FSSpecTreeModel(
    widgets.filesystemmodel.FileSystemModelMixin, itemmodels.ColumnItemModel
):
    """Tree model to display filesystems supported by fsspec.

    The model offers the same API as QFileSystemModel so that it can work
    easily as a drop-in replacement. Differences:

    * on windows, fsspec does not support a "real" root folder (a listing of drives)
    * the model does not watch for changes, use `refresh()` to update a folder.
    * `fileInfo()` / `rootDirectory()` only make sense for the local filesystem.

    ### Example

    ```py
    model = FSSpecTreeModel("github", org="phil65", repo="prettyqt")
    model = FSSpecTreeModel("memory")
    model = FSSpecTreeModel("s3://bucket/folder")
    model = FSSpecTreeModel(fsspec.filesystem("file"), root="/home")
    ```
    """

    SUPPORTS = FsSpecProtocolStr | fsspec.AbstractFileSystem
    DEFAULT_COLUMNS: ClassVar[list[type[FsSpecColumnItem]]] = [
        NameColumn,
        SizeColumn,
        TypeColumn,
    ]
    EXTRA_COLUMNS: ClassVar[list[type[FsSpecColumnItem]]] = [
        PathColumn,
        CreatedColumn,
        ModifiedColumn,
        PermissionsColumn,
        IsLinkColumn,
        ShaColumn,
    ]

    directoryLoaded = core.Signal(str)  # noqa: N815
    fileRenamed = core.Signal(str, str, str)  # noqa: N815
    rootPathChanged = core.Signal(str)  # noqa: N815

    class Roles(enum.IntEnum):
        FileIconRole = constants.DECORATION_ROLE
        FilePathRole = constants.USER_ROLE + 1
        FileNameRole = constants.USER_ROLE + 2
        FilePermissions = constants.USER_ROLE + 3
        ProtocolPathRole = constants.USER_ROLE + 4

    Option = widgets.QFileSystemModel.Option

    def __init__(
        self,
        obj: str | fsspec.AbstractFileSystem | UPath = "file",
        root: datatypes.PathType = "",
        show_root: bool = False,
        read_only: bool = False,
        parent: core.QObject | None = None,
        **kwargs: Any,
    ):
        """Create a model for given filesystem.

        Arguments:
            obj: fsspec filesystem, UPath, URL ("s3://bucket/path")
                 or protocol name ("memory", "github", ...)
            root: Root path (default: root of the filesystem / the URL path)
            show_root: Whether to show the root folder as an item.
            read_only: Whether the model allows renaming / drag & drop.
            parent: parent QObject
            kwargs: storage options for the filesystem (if obj is a string)
        """
        match obj:
            case str() if "://" in obj:
                self.fs, path = fsspec.url_to_fs(obj, **kwargs)
                self.root = path or self.fs.root_marker
            case str():
                self.fs = _get_filesystem(obj, **kwargs)
                self.root = self.fs.root_marker
            case fsspec.AbstractFileSystem():
                self.fs = obj
                self.root = self.fs.root_marker
            case _:  # UPath
                self.fs = obj.fs
                self.root = obj.path
        if root:
            self.root = os.fspath(root)
        # these need to exist before super().__init__ fetches the root folder.
        self._read_only = read_only
        self._options = self.Option(0)
        self._resolve_symlinks = True
        self._filter = DEFAULT_FILTER
        self._name_filters: list[str] = []
        self._name_filter_disables = True
        self._sort_column = 0
        self._sort_order = constants.ASCENDING
        root_info = self._get_info(self.root)
        columns = self.DEFAULT_COLUMNS + self._get_extra_columns()
        super().__init__(
            root_info,
            columns=columns,
            parent=parent,
            show_root=show_root,
            read_only=read_only,
        )

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, fsspec.AbstractFileSystem)

    # helpers

    @property
    def is_local(self) -> bool:
        protocols = (
            (self.fs.protocol,) if isinstance(self.fs.protocol, str) else self.fs.protocol
        )
        return "file" in protocols or "local" in protocols

    def _get_info(self, path: str) -> dict[str, Any]:
        try:
            info = self.fs.info(path)
        except FileNotFoundError, NotImplementedError:
            info = {"name": path, "type": "directory"}
        return self._normalize_info(info, path)

    def _normalize_info(self, info: dict, path: str) -> dict[str, Any]:
        """Normalize info dict to have consistent structure across filesystems."""
        normalized = dict(info)
        # Ensure name is the path, not a model/module name
        if "name" not in normalized or not self._is_path_like(normalized.get("name", "")):
            normalized["name"] = path
        normalized.setdefault("size", 0)
        return normalized

    def _is_path_like(self, value: str) -> bool:
        """Check if value looks like a path rather than a name."""
        if not value:
            return True  # Empty string is valid root
        return "/" in value or value == self.fs.root_marker

    def _get_extra_columns(self) -> list[type[FsSpecColumnItem]]:
        protocol = (
            self.fs.protocol if isinstance(self.fs.protocol, str) else self.fs.protocol[0]
        )
        get_fields = getattr(self.fs, "get_info_fields", None)
        # info dict keys which differ from the column identifiers
        key_map = {"islink": "is_link"}
        if get_fields and (fields := get_fields()):
            columns = {key_map.get(field, field) for field in fields}
        else:
            match protocol:
                case "github":
                    columns = {"sha"}
                case "file" | "local":
                    columns = {"path", "created", "mtime", "mode", "is_link"}
                case "smb":
                    columns = {"mtime"}
                case "memory":
                    columns = {"created"}
                case _:
                    return list(self.EXTRA_COLUMNS)
        return [col for col in self.EXTRA_COLUMNS if col.identifier in columns]

    def join(self, folder: str, name: str) -> str:
        """Join a folder path and a file name using the filesystem separator."""
        sep = getattr(self.fs, "sep", "/")
        return f"{folder.rstrip(sep)}{sep}{name}" if folder else name

    def get_file_name(self, path: str) -> str:
        """Return the last part of given path (the path itself for the root)."""
        sep = getattr(self.fs, "sep", "/")
        return path.rstrip(sep).rsplit(sep, 1)[-1] or path

    def is_dir_info(self, info: dict[str, Any]) -> bool:
        match info.get("type"):
            case "directory":
                return True
            case "file":
                return False
        # unknown types (like "other" / "link"), ask the filesystem.
        try:
            return self.fs.isdir(info["name"])
        except OSError, NotImplementedError:
            return False

    def get_icon(self, info: dict[str, Any]) -> gui.QIcon:
        if self.is_local:
            return _icon_provider.icon(core.QFileInfo(info["name"]))
        icon_type = (
            widgets.QFileIconProvider.IconType.Folder
            if self.is_dir_info(info)
            else widgets.QFileIconProvider.IconType.File
        )
        return _icon_provider.icon(icon_type)

    def get_permission_flags(self, info: dict[str, Any]) -> core.QFileDevice.Permission:
        flag = core.QFileDevice.Permission(0)
        if (mode := info.get("mode")) is None:
            return flag
        for i in core.filedevice.PERMISSIONS.get_list(int(mode) & 0o7777):
            flag |= core.filedevice.PERMISSIONS[i]
        return flag

    def _item_for(self, index: core.ModelIndex | str) -> FSSpecTreeModel.TreeItem | None:
        if isinstance(index, str):
            index = self.index(index)
        return index.internalPointer() if index.isValid() else None

    def _is_hidden(self, name: str) -> bool:
        return self.get_file_name(name).startswith(".")

    def _matches_name_filters(self, name: str) -> bool:
        if not self._name_filters:
            return True
        name = self.get_file_name(name)
        if self._filter & Filter.CaseSensitive:
            return any(fnmatch.fnmatchcase(name, f) for f in self._name_filters)
        name = name.lower()
        return any(fnmatch.fnmatchcase(name, f.lower()) for f in self._name_filters)

    def _accept(self, info: dict[str, Any]) -> bool | None:
        """Check whether info passes the filters.

        Returns True if accepted, None if it should be shown disabled
        (name filters with nameFilterDisables) and False if rejected.
        """
        name = info["name"]
        is_dir = self.is_dir_info(info)
        flt = self._filter
        if is_dir and not flt & (Filter.Dirs | Filter.AllDirs):
            return False
        if not is_dir and not flt & Filter.Files:
            return False
        if self._is_hidden(name) and not flt & Filter.Hidden:
            return False
        if info.get("islink") and flt & Filter.NoSymLinks:
            return False
        name_filtered = not (is_dir and flt & Filter.AllDirs)
        if name_filtered and not self._matches_name_filters(name):
            return None if self._name_filter_disables else False
        return True

    def _sort_key(self, item: FSSpecTreeModel.TreeItem):
        col = self._attr_cols[self._sort_column]
        value = col.get_data(item, constants.SORT_ROLE)
        if value is None:
            value = col.get_data(item, constants.DISPLAY_ROLE)
        match value:
            case None:
                value = (2, "")
            case int() | float():
                value = (0, value)
            case dt.datetime():
                value = (0, value.timestamp())
            case _:
                value = (1, str(value).lower())
        # folders first, like QFileSystemModel.
        is_dir = self.is_dir_info(item.obj)
        if self._sort_order == constants.DESCENDING:
            return (is_dir, value)
        return (not is_dir, value)

    def _sorted(self, items: list) -> list:
        reverse = self._sort_order == constants.DESCENDING
        return sorted(items, key=self._sort_key, reverse=reverse)

    # TreeModel overrides

    def _has_children(self, item: FSSpecTreeModel.TreeItem) -> bool:
        return self.is_dir_info(item.obj)

    def _fetch_object_children(
        self, item: FSSpecTreeModel.TreeItem
    ) -> list[FSSpecTreeModel.TreeItem]:
        path = item.obj["name"]
        try:
            children = self.fs.ls(path, detail=True)
        except OSError, NotImplementedError:
            logger.debug("Could not list %s", path)
            children = []
        items = []
        for child in children:
            name = child.get("name", "")
            if self.get_file_name(name) in {".", ".."}:
                continue
            # prepend parent path if name is not a full path
            if not self._is_path_like(name):
                name = self.join(path, name)
            info = self._normalize_info(child, name)
            info["name"] = name
            match self._accept(info):
                case False:
                    continue
                case None:
                    info["_disabled"] = True
            items.append(self.TreeItem(obj=info))
        self.directoryLoaded.emit(path)
        return self._sorted(items)

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        flags = super().flags(index)
        if not index.isValid():
            return flags if self._read_only else flags | constants.DROP_ENABLED
        item = index.internalPointer()
        if item.obj.get("_disabled"):
            return flags & ~constants.IS_ENABLED
        flags |= constants.DRAG_ENABLED
        if not self._read_only and self.is_dir_info(item.obj):
            flags |= constants.DROP_ENABLED
        return flags

    def sort(self, column: int, order: constants.SortOrder = constants.ASCENDING):
        """Sort all loaded folders by given column (folders first)."""
        if not 0 <= column < len(self._attr_cols):
            return
        self._sort_column = column
        self._sort_order = order
        self.layoutAboutToBeChanged.emit()
        old_indexes = self.persistentIndexList()
        items = [(idx.internalPointer(), idx.column()) for idx in old_indexes]
        stack = [self.inspected_item]
        while stack:
            tree_item = stack.pop()
            if tree_item.children_fetched and tree_item.children:
                tree_item.children = self._sorted(tree_item.children)
                stack.extend(tree_item.children)
        new_indexes = [self.createIndex(item.row(), col, item) for item, col in items]
        self.changePersistentIndexList(old_indexes, new_indexes)
        self.layoutChanged.emit()

    # Refreshing / modifying

    def refresh(self, index: core.ModelIndex | str | None = None):
        """Reload the children of given folder index (default: root folder)."""
        if isinstance(index, str):
            index = self.index(index)
        index = index or core.ModelIndex()
        if not index.isValid() and self._show_root:
            index = self.index(0, 0)
        index = index.siblingAtColumn(0) if index.isValid() else index
        item = self.data_by_index(index)
        with contextlib.suppress(Exception):
            self.fs.invalidate_cache(item.obj["name"])
        if item.children:
            with self.remove_rows(0, len(item.children) - 1, index):
                item.children.clear()
        item.children_fetched = False
        self.fetchMore(index)

    def _refresh_path(self, path: str):
        """Refresh folder with given path if it is loaded."""
        if (index := self._find_index(path, fetch=False)).isValid() or (
            path.rstrip("/") == self.rootPath().rstrip("/")
        ):
            self.refresh(index)

    def mkdir(self, parent: core.QModelIndex | str, name: str) -> core.ModelIndex:
        """Create a folder in given parent folder, return its index."""
        if isinstance(parent, str):
            parent = self.index(parent)
        parent_item = self.data_by_index(parent)
        path = self.join(parent_item.obj["name"], name)
        try:
            self.fs.mkdir(path)
        except OSError, NotImplementedError:
            logger.exception("Could not create folder %s", path)
            return core.ModelIndex()
        self.refresh(parent)
        return self.index(path)

    def _remove_index(self, index: core.QModelIndex | str, func) -> bool:
        if isinstance(index, str):
            index = self.index(index)
        if not index.isValid() or self._read_only:
            return False
        path = index.internalPointer().obj["name"]
        try:
            func(path)
        except OSError, NotImplementedError:
            logger.exception("Could not remove %s", path)
            return False
        with self.remove_row(index.row(), index.parent()):
            index.internalPointer().parent_item.children.pop(index.row())
        return True

    def remove(self, index: core.QModelIndex | str) -> bool:
        """Remove file / folder (recursively) at given index."""
        return self._remove_index(index, lambda p: self.fs.rm(p, recursive=True))

    def rmdir(self, index: core.QModelIndex | str) -> bool:
        """Remove the (empty) folder at given index."""
        return self._remove_index(index, self.fs.rmdir)

    def rename_item(self, item: FSSpecTreeModel.TreeItem, new_name: str) -> bool:
        path = item.obj["name"]
        folder = path.rstrip("/").rsplit("/", 1)[0] if "/" in path else ""
        old_name = self.get_file_name(path)
        if self._read_only or not new_name or new_name == old_name:
            return False
        target = self.join(folder, new_name)
        try:
            self.fs.mv(path, target, recursive=True)
        except OSError, NotImplementedError:
            logger.exception("Could not rename %s", path)
            return False
        item.obj = self._get_info(target)
        # children (if loaded) still have the old paths.
        item.children.clear()
        item.children_fetched = False
        self.fileRenamed.emit(folder, old_name, new_name)
        return True

    def rename(self, index: core.QModelIndex | str, value: str) -> bool:
        item = self._item_for(index)
        if item is None or not self.rename_item(item, value):
            return False
        index = self.index_for_item(item)
        self.dataChanged.emit(index, index.siblingAtColumn(self.columnCount() - 1))
        return True

    # QFileSystemModel API

    def get_protocol_path(self, index: core.QModelIndex | str) -> str:
        """Get the full URL (including protocol) for given index or path."""
        path = index if isinstance(index, str) else index.data(self.Roles.FilePathRole)
        return self.fs.unstrip_protocol(path)

    def get_file_content(self, index_or_path: str | core.QModelIndex) -> bytes:
        path = (
            index_or_path
            if isinstance(index_or_path, str)
            else index_or_path.data(self.Roles.FilePathRole)
        )
        return self.fs.cat_file(path)

    def fileIcon(self, index: core.QModelIndex | str) -> gui.QIcon:
        item = self._item_for(index)
        return gui.QIcon() if item is None else self.get_icon(item.obj)

    def fileInfo(self, index: core.QModelIndex | str) -> core.FileInfo | None:
        """Return a FileInfo for given index. (only meaningful for local paths)."""
        item = self._item_for(index)
        return None if item is None else core.FileInfo(item.obj["name"])

    def fileName(self, index: core.QModelIndex | str) -> str:
        item = self._item_for(index)
        return "" if item is None else self.get_file_name(item.obj["name"])

    def filePath(self, index: core.QModelIndex | str) -> str:
        item = self._item_for(index)
        return "" if item is None else item.obj["name"]

    def isDir(self, index: core.QModelIndex | str) -> bool:
        item = self._item_for(index)
        return item is not None and self.is_dir_info(item.obj)

    def size(self, index: core.QModelIndex | str) -> int:
        item = self._item_for(index)
        return 0 if item is None else item.obj.get("size") or 0

    def type(self, index: core.QModelIndex | str) -> str:
        item = self._item_for(index)
        return "" if item is None else item.obj.get("type") or ""

    def lastModified(self, index: core.QModelIndex | str) -> dt.datetime | None:
        item = self._item_for(index)
        return None if item is None else _to_datetime(item.obj.get("mtime"))

    def permissions(self, index: core.QModelIndex | str) -> core.QFileDevice.Permission:
        item = self._item_for(index)
        if item is None:
            return core.QFileDevice.Permission(0)
        return self.get_permission_flags(item.obj)

    def setRootPath(self, path: str | os.PathLike[str] | None) -> core.ModelIndex:
        self.root = os.fspath(path) if path else self.fs.root_marker
        self.set_root_item(self._get_info(self.root))
        self.rootPathChanged.emit(self.root)
        return self.index(0, 0) if self._show_root else core.ModelIndex()

    def rootPath(self) -> str:
        return self.inspected_item.obj["name"]

    def rootDirectory(self) -> core.Dir:
        """Return the root as a Dir. (only meaningful for local paths)."""
        return core.Dir(self.rootPath())

    def index(
        self,
        path_or_row: str | int,
        column: int = 0,
        parent: core.QModelIndex | None = None,
    ) -> core.ModelIndex:
        """Return index for given row/column/parent or for given path."""
        if isinstance(path_or_row, int):
            return super().index(path_or_row, column, parent)
        return self._find_index(path_or_row, column)

    def _find_index(
        self, target: str, column: int = 0, fetch: bool = True
    ) -> core.ModelIndex:
        """Find index for given path, fetching the folders on the way if fetch=True."""
        sep = getattr(self.fs, "sep", "/")
        target = os.fspath(target).rstrip(sep) or target
        parent = core.ModelIndex()
        while True:
            if fetch and self.canFetchMore(parent):
                self.fetchMore(parent)
            for i in range(self.rowCount(parent)):
                index = super().index(i, 0, parent)
                path = index.internalPointer().obj["name"].rstrip(sep)
                if path == target:
                    return index.siblingAtColumn(column)
                if target.startswith(path + sep) or (not path and self._show_root):
                    parent = index
                    break
            else:
                return core.ModelIndex()

    def roleNames(self) -> dict[int, core.QByteArray]:
        return {
            constants.DISPLAY_ROLE: core.QByteArray(b"display"),
            constants.DECORATION_ROLE: core.QByteArray(b"fileIcon"),
            constants.EDIT_ROLE: core.QByteArray(b"edit"),
            constants.TOOLTIP_ROLE: core.QByteArray(b"toolTip"),
            constants.STATUSTIP_ROLE: core.QByteArray(b"statusTip"),
            constants.WHATS_THIS_ROLE: core.QByteArray(b"whatsThis"),
            self.Roles.FilePathRole: core.QByteArray(b"filePath"),
            self.Roles.FileNameRole: core.QByteArray(b"fileName"),
            self.Roles.FilePermissions: core.QByteArray(b"filePermissions"),
        }

    def setReadOnly(self, val: bool):
        self._read_only = val

    def isReadOnly(self) -> bool:
        return self._read_only

    def setOption(self, option: widgets.QFileSystemModel.Option, on: bool = True):
        """Options are stored for compatibility, the model does not watch for changes."""
        self._options = self._options | option if on else self._options & ~option

    def options(self) -> widgets.QFileSystemModel.Option:
        return self._options

    def setOptions(self, options: widgets.QFileSystemModel.Option):
        self._options = options

    def testOption(self, option: widgets.QFileSystemModel.Option) -> bool:
        return bool(self._options & option)

    def resolveSymlinks(self) -> bool:
        return self._resolve_symlinks

    def setResolveSymlinks(self, enable: bool):
        self._resolve_symlinks = enable

    def setNameFilterDisables(self, enable: bool):
        self._name_filter_disables = enable
        self._apply_filters()

    def nameFilterDisables(self) -> bool:
        return self._name_filter_disables

    def setNameFilters(self, filters: Iterable[str]):
        self._name_filters = list(filters)
        self._apply_filters()

    def nameFilters(self) -> list[str]:
        return self._name_filters

    def setFilter(self, filters: core.QDir.Filter):
        self._filter = filters
        self._apply_filters()

    def filter(self) -> core.QDir.Filter:
        return self._filter

    def _apply_filters(self):
        # only rebuild once initialized.
        if hasattr(self, "_attr_cols"):
            self.set_root_item(self.inspected_item.obj)

    readOnly = core.Property(  # noqa: N815
        bool,
        isReadOnly,
        setReadOnly,
        doc="Used to set model to read-only",
    )

    # Drag & drop

    def mimeTypes(self) -> list[str]:
        return [PATHS_MIME_TYPE, "text/uri-list"]

    def mimeData(self, indexes: Iterable[core.ModelIndex]) -> core.QMimeData:
        paths = list(
            dict.fromkeys(i.data(self.Roles.FilePathRole) for i in indexes if i.isValid())
        )
        mime_data = core.MimeData()
        mime_data.setData(PATHS_MIME_TYPE, json.dumps(paths).encode())
        urls = [core.QUrl(self.get_protocol_path(p)) for p in paths]
        mime_data.setUrls(urls)
        return mime_data

    def supportedDragActions(self) -> constants.DropAction:
        return constants.DropAction.MoveAction | constants.DropAction.CopyAction

    def supportedDropActions(self) -> constants.DropAction:
        return constants.DropAction.MoveAction | constants.DropAction.CopyAction

    def _get_dropped_paths(self, mime_data: core.QMimeData) -> list[str]:
        if mime_data.hasFormat(PATHS_MIME_TYPE):
            return json.loads(mime_data.data(PATHS_MIME_TYPE).data().decode())
        if self.is_local and mime_data.hasUrls():
            return [u.toLocalFile() for u in mime_data.urls() if u.isLocalFile()]
        return []

    def canDropMimeData(
        self,
        mime_data: core.QMimeData,
        action: constants.DropAction,
        row: int,
        column: int,
        parent_index: core.QModelIndex,
    ) -> bool:
        if self._read_only or action not in (
            constants.DropAction.MoveAction,
            constants.DropAction.CopyAction,
        ):
            return False
        return bool(self._get_dropped_paths(mime_data))

    def _get_drop_folder(self, parent_index: core.QModelIndex) -> str:
        if not parent_index.isValid():
            return self.rootPath()
        info = parent_index.internalPointer().obj
        if self.is_dir_info(info):
            return info["name"]
        return info["name"].rstrip("/").rsplit("/", 1)[0]

    def dropMimeData(
        self,
        mime_data: core.QMimeData,
        action: constants.DropAction,
        row: int,
        column: int,
        parent_index: core.QModelIndex,
    ) -> bool:
        if not self.canDropMimeData(mime_data, action, row, column, parent_index):
            return False
        folder = self._get_drop_folder(parent_index)
        source_folders = set()
        changed = False
        for path in self._get_dropped_paths(mime_data):
            target = self.join(folder, self.get_file_name(path))
            # skip dropping onto itself / into own subfolder
            if path in (target, folder) or folder.startswith(path + "/"):
                continue
            try:
                if action == constants.DropAction.MoveAction:
                    self.fs.mv(path, target, recursive=True)
                    source_folders.add(path.rstrip("/").rsplit("/", 1)[0])
                else:
                    self.fs.copy(path, target, recursive=True)
            except OSError, NotImplementedError:
                logger.exception("Could not drop %s to %s", path, target)
                continue
            changed = True
        for source_folder in source_folders - {folder}:
            self._refresh_path(source_folder)
        if changed:
            self._refresh_path(folder)
        return changed


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    model = FSSpecTreeModel("github", org="phil65", repo="prettyqt")
    tree = widgets.TreeView()
    tree.setRootIsDecorated(True)
    tree.setup_dragdrop_move()
    tree.setAlternatingRowColors(True)
    tree.set_model(model)
    tree.setSortingEnabled(True)
    tree.set_selection_behavior("rows")
    tree.setUniformRowHeights(True)
    tree.setAnimated(True)
    tree.show()
    with app.debug_mode():
        app.exec()
