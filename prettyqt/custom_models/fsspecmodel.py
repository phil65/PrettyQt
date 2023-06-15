from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import datetime
import enum
import itertools
import logging
import os
import pathlib
from typing import TypedDict

import fsspec

from prettyqt import constants, core, gui, custom_models, widgets
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


@dataclass  # (frozen=True)
class FsSpecColumnItem(custom_models.ColumnItem):
    identifier: str = ""

    def get_user_data(self, tree_item, role):
        match role:
            case FSSpecTreeModel.Roles.FilePathRole:
                return tree_item.obj["name"]
            case FSSpecTreeModel.Roles.FilePathRole:
                return get_filename(treeitem.obj["name"])
            case FSSpecTreeModel.Roles.FilePermissions:
                return self.model.permissions(tree_item.obj["name"])
            case FSSpecTreeModel.Roles.ProtocolPathRole:
                return self.model.get_protocol_path(tree_item.obj["name"])


loc = core.Locale()


ATTR_MODEL_NAME = FsSpecColumnItem(
    identifier="name",
    name="Name",
    doc="The name of the object.",
    label=lambda x: get_filename(x.obj["name"]),
    set_edit=lambda x, value: x.set_name(value),
    decoration=lambda x: _icon_provider.get_icon(core.FileInfo(x.obj["name"])),
)


ATTR_MODEL_PATH = FsSpecColumnItem(
    identifier="name",
    name="Path",
    doc="A path",
    label=lambda x: x.obj["name"] or "",
)

ATTR_MODEL_SIZE = FsSpecColumnItem(
    identifier="size",
    name="Size",
    doc="Item size.",
    label=lambda x: loc.get_formatted_data_size(x.obj["size"])
    if x.obj["size"] > 0
    else "",
    sort_value=lambda x: x.obj["size"],
)

ATTR_MODEL_TYPE = FsSpecColumnItem(
    identifier="type",
    name="Type",
    doc="Item type.",
    label=lambda x: x.obj["type"] or "",
)

ATTR_MODEL_CREATED = FsSpecColumnItem(
    identifier="created",
    name="Created",
    doc="Date created.",
    label=lambda x: datetime.datetime.fromtimestamp(x.obj["created"])
    if x.obj.get("created")
    else "",
)

ATTR_MODEL_MODIFIED = FsSpecColumnItem(
    identifier="mtime",
    name="Modified",
    doc="Date modified.",
    label=lambda x: datetime.datetime.fromtimestamp(x.obj["mtime"])
    if x.obj.get("mtime")
    else "",
)

ATTR_MODEL_PERMISSIONS = FsSpecColumnItem(
    identifier="mode",
    name="Permissions",
    doc="File permissions.",
    label=lambda x: oct(int(x.obj["mode"]))[-4:] if x.obj.get("mode") else "",
)

ATTR_MODEL_IS_LINK = FsSpecColumnItem(
    identifier="islink",
    name="Link",
    doc="Symbolic link.",
    checkstate=lambda x: x.obj.get("islink") or False,
)

ATTR_MODEL_SHA = FsSpecColumnItem(
    identifier="sha",
    name="SHA",
    doc="SHA",
    label=lambda x: x.obj.get("sha") or "",
)

COLUMNS = [
    ATTR_MODEL_NAME,
    ATTR_MODEL_PATH,
    ATTR_MODEL_TYPE,
    ATTR_MODEL_MODIFIED,
    ATTR_MODEL_SIZE,
    ATTR_MODEL_CREATED,
    ATTR_MODEL_PERMISSIONS,
    ATTR_MODEL_IS_LINK,
    ATTR_MODEL_SHA,
]


class FSSpecTreeModel(
    widgets.filesystemmodel.FileSystemModelMixin, custom_models.ColumnItemModel
):
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
                    for col in COLUMNS
                    if col.identifier in {"name", "mode", "type", "size", "sha"}
                ]
            case "file":
                return [col for col in COLUMNS if col.identifier != "sha"]
            case _:
                return COLUMNS

    def _fetch_object_children(self, obj: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        """Fetch the children of a Python object.

        Returns: list of TreeItems
        """
        glob = f"{obj.obj['name']}/*/" if obj.obj["name"] else "*"
        items = [
            treeitem.TreeItem(obj=i, parent=obj)
            for i in self.fs.glob(glob, detail=True).values()
        ]
        # not sure if this should be emitted later?
        self.directoryLoaded.emit(obj.obj["name"])
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

    def flags(self, index):
        return super().flags(index) | constants.DROP_ENABLED | constants.DRAG_ENABLED

    # def dragEnterEvent(self, event):
    #     event.accept() if event.mimeData().hasUrls() else super().dragEnterEvent(event)

    def hasChildren(self, parent: core.ModelIndex | None = None) -> bool:
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return False
        item = self.data_by_index(parent)
        if self._show_root and item == self._root_item:
            return True
        return item.obj["type"] == "directory"

    def removeRows(self, row: int, count: int, parent: core.Modelindex):
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
                            "move", i, "to", parent_index.data(self.Roles.FilePathRole)
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
        app.main_loop()
