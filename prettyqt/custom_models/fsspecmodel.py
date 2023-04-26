from __future__ import annotations

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
    user_data={constants.USER_ROLE: lambda volume: str(volume.get_root_path())},
)


ATTR_MODEL_PATH = custom_models.ColumnItem(
    name="Path",
    doc="A path",
    label=lambda x: x.obj["name"] if x.obj["name"] else "",
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
    label=lambda x: x.obj["type"] if x.obj["type"] else "",
)

ATTR_MODEL_CREATED = custom_models.ColumnItem(
    name="Created",
    doc="Date created.",
    label=lambda x: x.obj["created"] if x.obj.get("created") else "",
)

ATTR_MODEL_IS_LINK = custom_models.ColumnItem(
    name="Link",
    label="",
    doc="Date created.",
    checkstate=lambda x: x.obj["islink"] if x.obj.get("islink") else False,
)


COLUMNS = [
    ATTR_MODEL_NAME,
    ATTR_MODEL_PATH,
    ATTR_MODEL_TYPE,
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
        self.rowsAboutToBeInserted.connect(self.fileIcon)
        self._show_root = show_root
        self.fs = fs
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

    def fileName(self, index):
        tree_item = index.internalPointer()
        return None if tree_item is None else pathlib.Path(tree_item.obj["name"]).name

    def filePath(self, index):
        tree_item = index.internalPointer()
        return None if tree_item is None else tree_item.obj["name"]

    def isDir(self, index):
        tree_item = index.internalPointer()
        return None if tree_item is None else tree_item.obj["type"] == "directory"

    def mkdir(self, index, name: str):
        tree_item = index.internalPointer()
        path = tree_item.obj["name"]
        new_folder = pathlib.Path(path) / name
        self.fs.mkdir(str(new_folder))

    def size(self, index):
        tree_item = index.internalPointer()
        return None if tree_item is None else tree_item.obj["size"]

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
        target = parent_folder / value
        self.fs.mv(path, target)
        self.fileRenamed.emit(parent_folder, old_name, value)


if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    from fsspec.implementations import local

    from prettyqt import widgets

    app = widgets.app()

    fs = local.LocalFileSystem()
    root = {"name": "C:/", "size": 0, "type": "directory"}
    print(fs.ls("C:/", detail=True))
    # fs = github.GithubFileSystem(org="phil65", repo="prettyqt", path="/")
    # root = {'name': 'prettyqt', 'size': 0, 'type': 'directory'}
    # print(root)

    model = FSSpecTreeModel(fs, root, False)
    tree = widgets.TreeView()
    tree.setRootIsDecorated(True)
    tree.setAlternatingRowColors(True)
    tree.set_model(model)
    tree.set_selection_behaviour("rows")
    tree.setUniformRowHeights(True)
    tree.setAnimated(True)
    tree.show()
    app.main_loop()
