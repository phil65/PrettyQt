from __future__ import annotations

from collections.abc import Iterable
import datetime
import enum
import itertools
import os
import pathlib
from typing import TypedDict

from prettyqt import constants, core, custom_models, widgets
from prettyqt.qt import QtCore
from prettyqt.utils import treeitem


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


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def get_filename(path):
    return pathlib.Path(path).name if path else ""


ATTR_MODEL_NAME = custom_models.ColumnItem(
    name="Name",
    doc="The name of the object.",
    label=lambda x: get_filename(x.obj["name"]),
    set_edit=lambda x, value: x.set_name(value),
    decoration=lambda x: _icon_provider.get_icon(core.FileInfo(x.obj["name"])),
    user_data={
        constants.USER_ROLE + 1: lambda x: x.obj["name"],
        constants.USER_ROLE + 2: lambda x: get_filename(x.obj["name"]),
    },
)


ATTR_MODEL_PATH = custom_models.ColumnItem(
    name="Path",
    doc="A path",
    label=lambda x: x.obj["name"] or "",
)

ATTR_MODEL_SIZE = custom_models.ColumnItem(
    name="Size",
    doc="Item size.",
    label=lambda x: sizeof_fmt(x.obj["size"]) if x.obj["size"] > 0 else "",
    sort_value=lambda x: x.obj["size"],
)

ATTR_MODEL_TYPE = custom_models.ColumnItem(
    name="Type",
    doc="Item type.",
    label=lambda x: x.obj["type"] or "",
)

ATTR_MODEL_CREATED = custom_models.ColumnItem(
    name="Created",
    doc="Date created.",
    label=lambda x: datetime.datetime.fromtimestamp(x.obj["created"])
    if x.obj.get("created")
    else "",
)

ATTR_MODEL_MODIFIED = custom_models.ColumnItem(
    name="Modified",
    doc="Date modified.",
    label=lambda x: datetime.datetime.fromtimestamp(x.obj["mtime"])
    if x.obj.get("mtime")
    else "",
)

ATTR_MODEL_PERMISSIONS = custom_models.ColumnItem(
    name="Permissions",
    doc="File permissions.",
    label=lambda x: oct(int(x.obj["mode"]))[-4:] if x.obj.get("mode") else "",
)

ATTR_MODEL_IS_LINK = custom_models.ColumnItem(
    name="Link",
    doc="Date created.",
    checkstate=lambda x: x.obj.get("islink") or False,
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
]


class FSSpecTreeModel(
    widgets.filesystemmodel.FileSystemModelMixin, custom_models.ColumnItemModel
):
    """Model that provides an interface to an objectree that is build of tree items."""

    directoryLoaded = core.Signal(str)
    fileRenamed = core.Signal(str, str, str)
    rootPathChanged = core.Signal(str)

    @core.Enum
    class Roles(enum.IntEnum):
        """Role enum."""

        FileIconRole = constants.DECORATION_ROLE
        FilePathRole = constants.USER_ROLE + 1
        FileNameRole = constants.USER_ROLE + 2
        FilePermissions = constants.USER_ROLE + 3

    @core.Enum
    class Option(enum.IntEnum):
        """Role enum."""

        DontWatchForChanges = 1
        DontResolveSymlinks = 2
        DontUseCustomDirectoryIcons = 4

    def __init__(
        self,
        fs,
        obj: FolderInfo,
        show_root: bool = False,
        parent: QtCore.QObject | None = None,
    ):
        self.fs = fs
        self.root_marker = fs.root_marker
        self.protocol = fs.protocol
        self.sep = fs.sep
        super().__init__(obj, columns=COLUMNS, parent=parent, show_root=show_root)

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

    def get_protocol_path(self, index: QtCore.QModelIndex) -> str:
        protocol = self.fs.protocol
        path = index.data(self.Roles.FilePathRole)
        return f"{protocol}://{path}"

    def fileIcon(self, index):
        tree_item = index.internalPointer()
        if tree_item is None:
            return None
        return _icon_provider.get_icon(core.FileInfo(tree_item.obj["name"]))

    def fileInfo(self, index):
        tree_item = index.internalPointer()
        return None if tree_item is None else core.FileInfo(tree_item.obj["name"])

    def fileName(self, index) -> str:
        tree_item = index.internalPointer()
        return "" if tree_item is None else pathlib.Path(tree_item.obj["name"]).name

    def filePath(self, index) -> str:
        tree_item = index.internalPointer()
        return "" if tree_item is None else tree_item.obj["name"]

    def isDir(self, index):
        tree_item = index.internalPointer()
        return False if tree_item is None else tree_item.obj["type"] == "directory"

    def mkdir(self, index, name: str):
        tree_item = index.internalPointer()
        path = tree_item.obj["name"]
        new_folder = pathlib.Path(path) / name
        self.fs.mkdir(str(new_folder))

    def size(self, index) -> int:
        tree_item = index.internalPointer()
        return 0 if tree_item is None else tree_item.obj["size"]

    def lastModified(self, index) -> int:
        tree_item = index.internalPointer()
        return (
            ""
            if tree_item is None
            else str(datetime.datetime.fromtimestamp(tree_item.obj["mtime"]))
        )

    def permissions(self, index) -> QtCore.QFileDevice.Permission:
        tree_item = index.internalPointer()
        flag = QtCore.QFileDevice.Permission(0)
        if tree_item is None:
            return flag
        val = oct(int(tree_item.obj["mode"]))[-4:]
        for i in core.filedevice.PERMISSIONS.get_list(int(val, 8)):
            flag |= core.filedevice.PERMISSIONS[i]
        return flag

    def remove(self, index) -> bool:
        tree_item = index.internalPointer()
        path = tree_item.obj["name"]
        self.fs.rm_file(path)
        return self.fs.exists(path)

    def rmdir(self, index) -> bool:
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
        paths = [i for idx in indexes if (i := idx.data(self.Roles.FilePathRole))]
        urls = [core.Url(i) for i in paths]
        mime_data.setUrls(urls)
        return mime_data

    def supportedDropActions(self):
        return (
            QtCore.Qt.DropAction.MoveAction
            | QtCore.Qt.DropAction.CopyAction
            | QtCore.Qt.DropAction.LinkAction
        )

    def flags(self, index):
        flags = super().flags(index)
        return flags | constants.DROP_ENABLED | constants.DRAG_ENABLED

    # def dragEnterEvent(self, event):
    #     event.accept() if event.mimeData().hasUrls() else super().dragEnterEvent(event)

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return False
        if self._show_root and self.tree_item(parent) == self._root_item:
            return True
        return self.tree_item(parent).obj["type"] == "directory"

    def removeRows(self, row: int, count: int, parent):
        print(row, count, parent.data())
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
        parent: QtCore.QModelIndex | None = None,
    ):
        if position is None:
            position = len(self.items)
        items = list(items)
        # with self.insert_rows(position, position + len(items) - 1, parent):
        #     for i in range(len(items)):
        #         self.items.insert(i + position, items[i])
        #         pass
        #     self.items.extend(items)
        return items

    def canDropMimeData(
        self,
        mime_data: QtCore.QMimeData,
        action: QtCore.Qt.DropAction,
        row: int,
        column: int,
        parent_index: QtCore.QModelIndex,
    ):
        return column == 0 and mime_data.hasFormat("text/uri-list")

    def dropMimeData(
        self,
        mime_data: QtCore.QMimeData,
        action: QtCore.Qt.DropAction,
        row: int,
        column: int,
        parent_index: QtCore.QModelIndex,
    ):
        if not self.canDropMimeData(mime_data, action, row, column, parent_index):
            return False
        print(mime_data.urls(), action, row, column, parent_index.data())
        urls = [core.Url(i) for i in mime_data.urls()]
        if not urls:
            return False
        if action == QtCore.Qt.DropAction.MoveAction:
            with self.change_layout():
                for i in sorted(urls, reverse=True):
                    # self.fs.mv(i, )
                    print("move", i, "to", parent_index.data(self.Roles.FilePathRole))
        elif action == QtCore.Qt.DropAction.CopyAction:
            pass
        elif action == QtCore.Qt.DropAction.LinkAction:
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
        index: QtCore.QModelIndex | None = None,
    ) -> core.ModelIndex:
        if isinstance(path_or_row, int):
            return super().index(path_or_row, column, index)
        return self._iter_path(path_or_row, column, index)

    def _iter_path(self, target: os.PathLike, column: int = 0, parent=None):
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

    def roleNames(self) -> dict[int, QtCore.QByteArray]:
        return {
            259: QtCore.QByteArray(b"filePermissions"),
            1: QtCore.QByteArray(b"fileIcon"),
            4: QtCore.QByteArray(b"statusTip"),
            3: QtCore.QByteArray(b"toolTip"),
            2: QtCore.QByteArray(b"edit"),
            257: QtCore.QByteArray(b"filePath"),
            0: QtCore.QByteArray(b"display"),
            258: QtCore.QByteArray(b"fileName"),
            5: QtCore.QByteArray(b"whatsThis"),
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


if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    import fsspec

    from prettyqt import widgets

    app = widgets.app()

    fs = fsspec.filesystem("file", org="phil65", repo="prettyqt", path="/")
    root = fs.info("")
    print(root, fs.ls("", detail=True))
    model = FSSpecTreeModel(fs, root, False)
    print(model.mimeTypes())
    tree = widgets.TreeView()
    tree.setRootIsDecorated(True)
    tree.setup_dragdrop_move()
    tree.setAlternatingRowColors(True)
    tree.set_model(model)
    tree.set_selection_behaviour("rows")
    tree.setUniformRowHeights(True)
    tree.setAnimated(True)
    tree.show()
    app.main_loop()
