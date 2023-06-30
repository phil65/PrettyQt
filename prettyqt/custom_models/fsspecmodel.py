from __future__ import annotations

from collections.abc import Iterable
import datetime
import enum
import itertools
import logging
import os
import pathlib

from typing import TypedDict

import fsspec

from prettyqt import constants, core, custom_models, gui, widgets
from prettyqt.utils import datatypes, treeitem


logger = logging.getLogger(__name__)


class FsSpecCompleter(widgets.Completer):
    def pathFromIndex(self, index):
        return index.data(self.model().Roles.FilePathRole)

    def splitPath(self, path: str):
        return path.split(self.model().fs.sep)


class FolderInfo(TypedDict):
    name: str
    size: int
    type: str
    created: float
    islink: bool  # symbolic link
    mode: int  # Inode protection mode.
    uid: int  # user id of owner
    gid: int  # group id of owner
    mtime: float
    ino: int  # Inode number.
    nlink: int  # Number of links to the inode.


_icon_provider = widgets.FileIconProvider()


VALUE_LETTERS = [(4, "r"), (2, "w"), (1, "x")]


def octal_to_string(octal: int) -> str:
    result = ""
    # Iterate over each of the digits in octal
    for digit, (value, letter) in itertools.product(
        [int(n) for n in str(octal)], VALUE_LETTERS
    ):
        if digit >= value:
            result += letter
            digit -= value
        else:
            result += "-"
    return result


def get_filename(path):
    return pathlib.Path(path).name if path else ""


class FsSpecColumnItem(custom_models.ColumnItem):
    identifier: str = ""

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        match role:
            case FSSpecTreeModel.Roles.FilePathRole:
                return item.obj["name"]
            case FSSpecTreeModel.Roles.FilePathRole:
                return get_filename(item.obj["name"])
            case FSSpecTreeModel.Roles.FilePermissions:
                return self.model.permissions(item.obj["name"])
            case FSSpecTreeModel.Roles.ProtocolPathRole:
                return self.model.get_protocol_path(item.obj["name"])


class NameColumn(FsSpecColumnItem):
    identifier = "name"
    name = "Name"
    doc = "File name"

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return pathlib.Path(path).name if (path := item.obj["name"]) else ""
            case constants.DECORATION_ROLE:
                return _icon_provider.get_icon(core.FileInfo(item.obj["name"]))
            case _:
                return super().get_data(item, role)

    def set_data(self, item, value, role):
        match role:
            case constants.EDIT_ROLE:
                item.set_name(value)


class PathColumn(FsSpecColumnItem):
    identifier = "path"
    name = "Path"
    doc = "File path"

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj["name"] or ""
            case _:
                return super().get_data(item, role)


class SizeColumn(FsSpecColumnItem):
    identifier = "size"
    name = "Size"
    doc = "File size."

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                if item.obj["size"] > 0:
                    return core.Locale().get_formatted_data_size(item.obj["size"])
                else:
                    return ""
            case constants.SORT_ROLE:
                return item.obj["size"]
            case _:
                return super().get_data(item, role)


class TypeColumn(FsSpecColumnItem):
    identifier = "type"
    name = "Type"
    doc = "Type of given path."

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj["type"] or ""
            case _:
                return super().get_data(item, role)


class CreatedColumn(FsSpecColumnItem):
    identifier = "created"
    name = "Created"
    doc = "Creation date of file."

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        if not item.obj.get("created"):
            return None
        created = datetime.datetime.fromtimestamp(item.obj["created"])
        match role:
            case constants.DISPLAY_ROLE:
                return created.strftime("%m/%d/%Y, %H:%M:%S")
            case constants.USER_ROLE:
                return created
            case _:
                return super().get_data(item, role)


class ModifiedColumn(FsSpecColumnItem):
    identifier = "mtime"
    name = "Modified"
    doc = "Modified"

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        if not item.obj.get("mtime"):
            return None
        mtime = datetime.datetime.fromtimestamp(item.obj["mtime"])
        match role:
            case constants.DISPLAY_ROLE:
                return mtime.strftime("%m/%d/%Y, %H:%M:%S")
            case constants.USER_ROLE:
                return mtime
            case _:
                return super().get_data(item, role)


class PermissionsColumn(FsSpecColumnItem):
    identifier = "mode"
    name = "Permissions"
    doc = "File Permissions"

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return oct(int(item.obj["mode"]))[-4:] if item.obj.get("mode") else ""
            case _:
                return super().get_data(item, role)


class IsLinkColumn(FsSpecColumnItem):
    identifier = "mode"
    name = "Is link"
    doc = "Whether file is a symbolic link."

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.CHECKSTATE_ROLE:
                return self.to_checkstate(item.obj.get("islink"))
            case _:
                return super().get_data(item, role)


class ShaColumn(FsSpecColumnItem):
    identifier = "sha"
    name = "SHA"
    doc = "Hash value."

    def get_data(self, item: treeitem.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj.get("sha") or ""
            case _:
                return super().get_data(item, role)


class FSSpecTreeModel(
    widgets.filesystemmodel.FileSystemModelMixin, custom_models.ColumnItemModel
):
    COLUMNS = [
        NameColumn,
        PathColumn,
        SizeColumn,
        TypeColumn,
        CreatedColumn,
        ModifiedColumn,
        PermissionsColumn,
        IsLinkColumn,
        ShaColumn,
    ]

    directoryLoaded = core.Signal(str)
    fileRenamed = core.Signal(str, str, str)
    rootPathChanged = core.Signal(str)

    class Roles(enum.IntEnum):
        """Role enum."""

        FileIconRole = constants.DECORATION_ROLE
        FilePathRole = constants.USER_ROLE + 1
        FileNameRole = constants.USER_ROLE + 2
        FilePermissions = constants.USER_ROLE + 3
        ProtocolPathRole = constants.USER_ROLE + 4

    class Option(enum.IntEnum):
        """Role enum."""

        DontWatchForChanges = 1
        DontResolveSymlinks = 2
        DontUseCustomDirectoryIcons = 4

    def __init__(
        self,
        protocol: str = "file",
        root: datatypes.PathType = "",
        show_root: bool = False,
        parent: core.QObject | None = None,
        **kwargs,
    ):
        self.set_protocol(protocol, **kwargs)
        obj = self.fs.info(root)
        columns = self._get_columns_for_protocol(protocol)
        super().__init__(obj, columns=columns, parent=parent, show_root=show_root)

    def set_protocol(self, protocol: str, **kwargs):
        self.fs = fsspec.filesystem(protocol, **kwargs)

    def _get_columns_for_protocol(self, protocol: str):
        match self.fs.protocol:
            case "github":
                return [
                    col
                    for col in self.COLUMNS
                    if col.identifier in {"name", "mode", "type", "size", "sha"}
                ]
            case "file":
                return [col for col in self.COLUMNS if col.identifier != "sha"]
            case _:
                return self.COLUMNS

    def _has_children(self, item: treeitem.TreeItem) -> bool:
        return item.obj["type"] == "directory"

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        """Fetch the children of a Python object.

        Returns: list of TreeItems
        """
        glob = f"{item.obj['name']}/*/" if item.obj["name"] else "*"
        items = [
            treeitem.TreeItem(obj=i, parent=item)
            for i in self.fs.glob(glob, detail=True).values()
        ]
        # not sure if this should be emitted later?
        self.directoryLoaded.emit(item.obj["name"])
        return items

    def get_protocol_path(self, index: core.QModelIndex | str) -> str:
        """Get protocol path for given index."""
        if isinstance(index, str):
            index = self.index(index)
        protocol = self.fs.protocol
        path = index.data(self.Roles.FilePathRole)
        return f"{protocol}://{path}"

    def get_file_content(self, index_or_path: str | core.QModelIndex):
        if isinstance(index_or_path, str):
            index = self.index(index_or_path)
        else:
            index = index_or_path
        protocol_path = self.get_protocol_path(index)
        # info = self.fs.info(protocol_path)
        with self.fs.open(protocol_path) as file:
            return file.read()

    def fileIcon(self, index: core.QModelIndex | str) -> gui.Icon:
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        if tree_item is None:
            return None
        return _icon_provider.get_icon(core.FileInfo(tree_item.obj["name"]))

    def fileInfo(self, index: core.QModelIndex | str):
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        return None if tree_item is None else core.FileInfo(tree_item.obj["name"])

    def fileName(self, index: core.QModelIndex) -> str:
        tree_item = index.internalPointer()
        return "" if tree_item is None else pathlib.Path(tree_item.obj["name"]).name

    def filePath(self, index: core.QModelIndex) -> str:
        tree_item = index.internalPointer()
        return "" if tree_item is None else tree_item.obj["name"]

    def isDir(self, index: core.QModelIndex | str):
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        return False if tree_item is None else tree_item.obj["type"] == "directory"

    def mkdir(self, index: core.QModelIndex | str, name: str):
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        path = tree_item.obj["name"]
        new_folder = pathlib.Path(path) / name
        self.fs.mkdir(str(new_folder))

    def size(self, index: core.QModelIndex | str) -> int:
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        return 0 if tree_item is None else tree_item.obj["size"]

    def lastModified(self, index: core.QModelIndex | str) -> datetime.datetime | None:
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        return (
            None
            if tree_item is None
            else datetime.datetime.fromtimestamp(tree_item.obj["mtime"])
        )

    def permissions(self, index: core.QModelIndex | str) -> core.QFileDevice.Permission:
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        flag = core.QFileDevice.Permission(0)
        if tree_item is None:
            return flag
        val = oct(int(tree_item.obj["mode"]))[-4:]
        for i in core.filedevice.PERMISSIONS.get_list(int(val, 8)):
            flag |= core.filedevice.PERMISSIONS[i]
        return flag

    def remove(self, index: core.QModelIndex | str) -> bool:
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        path = tree_item.obj["name"]
        self.fs.rm_file(path)
        return self.fs.exists(path)

    def rmdir(self, index: core.QModelIndex | str) -> bool:
        if isinstance(index, str):
            index = self.index(index)
        tree_item = index.internalPointer()
        path = tree_item.obj["name"]
        self.fs.rmdir(path)
        return self.fs.exists(path)

    def setRootPath(self, path: os.PathLike | None) -> core.ModelIndex:
        path = os.fspath(path) if path else self.fs.root_marker
        item = self.fs.info(path)
        self.set_root_item(item)
        self.rootPathChanged.emit(path)

    def rootDirectory(self) -> core.Dir:
        return core.Dir(self.rootPath())

    def rootPath(self) -> str:
        return self._root_item["name"]

    def rename(self, index, value: str):
        tree_item = index.internalPointer()
        path = tree_item.obj["name"]
        old_name = pathlib.Path(path).name
        parent_folder = pathlib.Path(path).parent
        target = str(parent_folder / value)
        self.fs.mv(path, target)
        exists = self.fs.exists(target)
        if exists:
            self.fileRenamed.emit(parent_folder, old_name, value)
        return exists

    def type(self, index) -> str:
        tree_item = index.internalPointer()
        return tree_item.obj["type"]

    def mimeTypes(self):
        return ["text/uri-list"]

    def mimeData(self, indexes):
        mime_data = core.MimeData()
        role = self.Roles.FilePathRole
        urls = [core.Url(i) for idx in indexes if (i := idx.data(role))]
        mime_data.setUrls(urls)
        return mime_data

    def supportedDropActions(self):
        DropAction = constants.DropAction
        return DropAction.MoveAction | DropAction.CopyAction | DropAction.LinkAction

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        return super().flags(index) | constants.DROP_ENABLED | constants.DRAG_ENABLED

    # def dragEnterEvent(self, event):
    #     event.accept() if event.mimeData().hasUrls() else super().dragEnterEvent(event)

    def removeRows(self, row: int, count: int, parent: core.ModelIndex):
        # end_row = row + count - 1
        # with self.remove_rows(row, end_row, parent):
        #     for i in range(end_row, row - 1, -1):
        #         self.items.pop(i)
        return True

    def remove_items(self, offsets: Iterable[int]):
        for offset in sorted(offsets, reverse=True):
            self.removeRow(offset)

    def add_items(
        self,
        items: Iterable,
        position: int | None = None,
        parent: core.QModelIndex | None = None,
    ):
        position = len(self.items) if position is None else position
        items = list(items)
        # with self.insert_rows(position, position + len(items) - 1, parent):
        #     for i in range(len(items)):
        #         self.items.insert(i + position, items[i])
        #         pass
        #     self.items.extend(items)
        return items

    def canDropMimeData(
        self,
        mime_data: core.QMimeData,
        action: constants.DropAction,
        row: int,
        column: int,
        parent_index: core.QModelIndex,
    ) -> bool:
        return column == 0 and mime_data.hasFormat("text/uri-list")

    def dropMimeData(
        self,
        mime_data: core.QMimeData,
        action: constants.DropAction,
        row: int,
        column: int,
        parent_index: core.QModelIndex,
    ):
        if not self.canDropMimeData(mime_data, action, row, column, parent_index):
            return False
        print(mime_data.urls(), action, row, column, parent_index.data())
        urls = [core.Url(i) for i in mime_data.urls()]
        if not urls:
            return False
        match action:
            case constants.DropAction.MoveAction:
                with self.change_layout():
                    for i in sorted(urls, reverse=True):
                        logger.info(
                            "move %s to %s", i, parent_index.data(self.Roles.FilePathRole)
                        )
            case constants.DropAction.CopyAction:
                pass
            case constants.DropAction.LinkAction:
                pass

        column = min(column, 0)
        if row != -1:
            begin_row = row
        elif parent_index.isValid():
            begin_row = self.rowCount(parent_index) + 1
        else:
            begin_row = self.rowCount() + 1
        print(begin_row)
        return True

        # if action == Qt.CopyAction:
        #     # Behavior if parent is a text item
        #     # For example, we select a text and do: CTRL+C CTRL+V
        #     if parent.isValid() and not parent.internalPointer().isFolder():
        #         # We insert copy in parent folder, just below
        #         begin_row = parent.row() + 1
        #         parent = parent.parent()

        #     if parent.isValid() and parent.internalPointer().isFolder():
        #         pass
        # if not items:
        #     return False

        # if action == Qt.CopyAction:
        #     pass

        # r = self.insertItems(items, begin_row, parent)
        # return r

        # return True

    # @functools.singledispatchmethod
    def index(
        self,
        path_or_row: str | int,
        column: int = 0,
        index: core.QModelIndex | None = None,
    ) -> core.ModelIndex:
        if isinstance(path_or_row, int):
            return super().index(path_or_row, column, index)
        return self._iter_path(path_or_row, column, index)

    def _iter_path(
        self,
        target: datatypes.PathType,
        column: int = 0,
        parent: core.ModelIndex | None = None,
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        target = pathlib.Path(target)
        row_count = self.rowCount(parent)
        for i in range(row_count):
            index = self.index(i, column, parent)
            path = self.filePath(index)
            path = pathlib.Path(path)
            if target == path:
                return index
            elif target.is_relative_to(path):
                if self.canFetchMore(index):
                    self.fetchMore(index)
                return self._iter_path(target, column, index)
        return core.ModelIndex()

    def roleNames(self) -> dict[int, core.QByteArray]:
        return {
            259: core.QByteArray(b"filePermissions"),
            1: core.QByteArray(b"fileIcon"),
            4: core.QByteArray(b"statusTip"),
            3: core.QByteArray(b"toolTip"),
            2: core.QByteArray(b"edit"),
            257: core.QByteArray(b"filePath"),
            0: core.QByteArray(b"display"),
            258: core.QByteArray(b"fileName"),
            5: core.QByteArray(b"whatsThis"),
        }

    def setReadOnly(self, val: bool):
        return NotImplemented

    def isReadOnly(self) -> bool:
        return NotImplemented

    def setOption(self, opt, val):
        return NotImplemented

    def options(self):
        return NotImplemented

    def testOption(self, opt):
        return NotImplemented

    def resolveSymlinks(self, val):
        return NotImplemented

    def setResolveSymlinks(self, val):
        return NotImplemented

    def setNameFilterDisables(self, value):
        return NotImplemented

    def nameFilterDisables(self):
        return NotImplemented

    def setNameFilters(self, filters):
        return NotImplemented

    def nameFilters(self):
        return NotImplemented

    def setFilter(self, filter):
        return NotImplemented

    def filter(self):
        return NotImplemented

    readOnly = core.Property(bool, isReadOnly, setReadOnly)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    model = FSSpecTreeModel("file", org="phil65", repo="prettyqt", path="/")
    # model.set_root_path("/")
    tree = widgets.TreeView()
    tree.setRootIsDecorated(True)
    tree.setup_dragdrop_move()
    tree.setAlternatingRowColors(True)
    tree.set_model(model)
    tree.set_selection_behavior("rows")
    tree.setUniformRowHeights(True)
    tree.setAnimated(True)
    tree.show()
    with app.debug_mode():
        app.exec()
