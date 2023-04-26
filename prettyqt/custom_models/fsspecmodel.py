from __future__ import annotations

import datetime
import enum
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


_icon_provider = widgets.FileIconProvider()


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
    label=lambda x: f"{(x.obj['size'] / (1024*1024)):.2f} MB"
    if x.obj["size"] > 0
    else "",
)

ATTR_MODEL_TYPE = custom_models.ColumnItem(
    name="Type",
    doc="Item type.",
    label=lambda x: x.obj["type"] or "",
)

ATTR_MODEL_CREATED = custom_models.ColumnItem(
    name="Created",
    doc="Date created.",
    label=lambda x: str(datetime.datetime.fromtimestamp(x.obj["created"]))
    if x.obj.get("created")
    else "",
)

ATTR_MODEL_MODIFIED = custom_models.ColumnItem(
    name="Modified",
    doc="Date modified.",
    label=lambda x: str(datetime.datetime.fromtimestamp(x.obj["mtime"]))
    if x.obj.get("mtime")
    else "",
)


ATTR_MODEL_IS_LINK = custom_models.ColumnItem(
    name="Link",
    label="",
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
    ATTR_MODEL_IS_LINK,
]


class FSSpecTreeModel(custom_models.ColumnItemModel):
    """Model that provides an interface to an objectree that is build of tree items."""

    directoryLoaded = core.Signal(str)
    fileRenamed = core.Signal(str, str, str)
    rootPathChanged = core.Signal(str)

    class Roles(enum.IntEnum):
        """Role enum."""

        FileIconRole = constants.DECORATION_ROLE
        FilePathRole = constants.USER_ROLE + 1
        FileNameRole = constants.USER_ROLE + 2
        FilePermissions = constants.USER_ROLE + 3

    core.Enum(Roles)

    def __init__(
        self,
        fs,
        obj: FolderInfo,
        show_root: bool = False,
        parent: QtCore.QObject | None = None,
    ):
        super().__init__(attr_cols=COLUMNS, parent=parent)
        self._show_root = show_root
        self.fs = fs
        self.root_marker = fs.root_marker
        if self._show_root:
            self._root_item = treeitem.TreeItem(obj=None)
            self._root_item.children_fetched = True
            self.inspected_item = treeitem.TreeItem(obj=obj)
            self._root_item.append_child(self.inspected_item)
        else:
            # The root itself will be invisible
            self._root_item = treeitem.TreeItem(obj=obj)
            self.inspected_item = self._root_item

            # Fetch all items of the root so we can select the first row in the ctor.
            root_index = self.index(0, 0)
            self.fetchMore(root_index)

    def _fetch_object_children(self, obj: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        """Fetch the children of a Python object.

        Returns: list of TreeItems
        """
        items = [
            treeitem.TreeItem(obj=i, parent=obj)
            for i in self.fs.glob(f"{obj.obj['name']}/*/", detail=True).values()
        ]
        # not sure if this should be emitted later?
        self.directoryLoaded.emit(obj.obj["name"])
        return items

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

    def setRootPath(self, path: os.PathLike) -> core.ModelIndex:
        path = os.fspath(path)
        self._root_item = {"name": path, "size": 0, "type": "directory"}
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

    def dragEnterEvent(self, event):
        event.accept() if event.mimeData().hasUrls() else super().dragEnterEvent(event)

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = core.ModelIndex() if parent is None else parent
        if parent.column() > 0:
            return False
        if self._show_root and self.tree_item(parent) == self._root_item:
            return True
        return self.tree_item(parent).obj["type"] == "directory"

    def canDropMimeData(
        self,
        mime_data: QtCore.QMimeData,
        action: QtCore.Qt.DropAction,
        row: int,
        column: int,
        parent_index: QtCore.QModelIndex,
    ):
        if not mime_data.hasFormat("text/uri-list"):
            return False
        if column > 0:
            return False
        return True

    def dropMimeData(
        self,
        mime_data: QtCore.QMimeData,
        action: QtCore.Qt.DropAction,
        row: int,
        column: int,
        parent_index: QtCore.QModelIndex,
    ):
        # if not mime_data.hasFormat("text/uri-list"):
        #     return False
        print(mime_data.urls(), action, row, column)

        # if action == Qt.IgnoreAction:
        #     return True  # What is that?

        # if action == Qt.MoveAction:
        #     # Strangely, on some cases, we get a call to dropMimeData though
        #     # self.canDropMimeData returned False.
        #     # See https://github.com/olivierkes/manuskript/issues/169 to reproduce.
        #     # So we double check for safety.
        #     if not self.canDropMimeData(data, action, row, column, parent):
        #         return False

        # items = mime_data.urls()

        # if not items:
        #     return False

        # if column > 0:
        #     column = 0

        # if row != -1:
        #     begin_row = row
        # elif parent.isValid():
        #     begin_row = self.rowCount(parent) + 1
        # else:
        #     begin_row = self.rowCount() + 1

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


if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    from fsspec.implementations import local

    from prettyqt import widgets

    app = widgets.app()

    fs = local.LocalFileSystem()
    root = {"name": "C:/", "size": 0, "type": "directory"}
    # fs = github.GithubFileSystem(org="phil65", repo="prettyqt", path="/")
    # root = {'name': 'prettyqt', 'size': 0, 'type': 'directory'}
    # print(root)

    model = FSSpecTreeModel(fs, root, False)
    print(model.mimeTypes())
    tree = widgets.TreeView()
    tree.setRootIsDecorated(True)
    tree.setup_dragdrop_move()
    tree.setAlternatingRowColors(True)
    tree.set_model(model)
    tree.set_selection_behaviour("rows")
    idx = model.index(
        "C:\\Users\\phili\\AppData\\Local\\Programs\\Python\\Python310\\Lib"
    )
    print(idx.isValid())
    print(idx.parent().parent().data(constants.DISPLAY_ROLE))
    tree.setUniformRowHeights(True)
    tree.setAnimated(True)
    tree.show()
    app.main_loop()
