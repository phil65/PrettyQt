from __future__ import annotations

import logging
import os
import pathlib
import time
from typing import TYPE_CHECKING, ClassVar

import git

from prettyqt import constants, itemmodels


if TYPE_CHECKING:
    from prettyqt import core


logger = logging.getLogger(__name__)


class GitPythonTreeModel(itemmodels.TreeModel):
    """Base Tree Model to display a file tree combined with Git information.

    ```py
    model = GitPythonTreeModel(PATH_TO_GIT_FOLDER)
    table = widgets.TreeView()
    table.set_model(model)
    table.show()
    ```
    """

    SUPPORTS = os.PathLike | str | git.Tree | git.Repo
    HEADER: ClassVar = [
        "Name",
        "Absolute path",
        "Type",
        "Size",
        "Hex SHA",
        "Mode",
        "Mime type",
    ]

    def __init__(self, path: os.PathLike[str] | str | git.Tree | git.Repo, **kwargs):
        match path:
            case os.PathLike() | str():
                tree = git.Repo(path).tree()
            case git.Tree():
                tree = path
            case git.Repo():
                tree = path.tree()
            case _:
                raise TypeError(path)
        super().__init__(tree, **kwargs)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE if section < len(
                self.HEADER
            ):
                return self.HEADER[section]
        return None

    def data(  # noqa: PLR0911
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        obj = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return obj.name
            case constants.DISPLAY_ROLE, 1:
                return obj.abspath
            case constants.DISPLAY_ROLE, 2:
                return obj.type
            case constants.DISPLAY_ROLE, 3:
                return str(obj.size)
            case constants.DISPLAY_ROLE, 4:
                return obj.hexsha
            case constants.DISPLAY_ROLE, 5:
                return oct(obj.mode)
            case constants.DISPLAY_ROLE, 6:
                return obj.mime_type if isinstance(obj, git.Blob) else ""
            case constants.USER_ROLE, _:
                return obj
        return None

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, git.Tree | git.Repo)

    def _fetch_object_children(
        self, item: GitPythonTreeModel.TreeItem
    ) -> list[GitPythonTreeModel.TreeItem]:
        if not isinstance(item.obj, git.Tree):
            return []
        return [self.TreeItem(obj=i) for i in item.obj.trees + item.obj.blobs]

    def _has_children(self, item: GitPythonTreeModel.TreeItem) -> bool:
        return isinstance(item.obj, git.Tree) and len(item.obj) > 0


class GitPythonCommitTreeModel(itemmodels.TreeModel):
    """Base Tree Model to display a file tree combined with Git information.

    ```py
    model = GitPythonCommitTreeModel(PATH_TO_GIT_FOLDER)
    table = widgets.TreeView()
    table.set_model(model)
    table.show()
    ```
    """

    SUPPORTS = os.PathLike | str | git.Repo | git.Commit
    HEADER: ClassVar = [
        "Date",
        "Hex SHA",
        "Author",
        "Summary",
    ]

    def __init__(
        self,
        repo: os.PathLike[str] | str | git.Tree | git.Repo | git.Commit,
        **kwargs,
    ):
        match repo:
            case os.PathLike() | str():
                commit = git.Repo(repo).head.commit
            case git.Repo():
                commit = repo.head.commit
            case git.Commit():
                commit = repo
            case _:
                raise TypeError(repo)
        super().__init__(commit, **kwargs)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        return len(self.HEADER)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE if section < len(
                self.HEADER
            ):
                return self.HEADER[section]
        return None

    def data(  # noqa: PLR0911
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        commit = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                gmtime = time.gmtime(commit.committed_date)
                return time.strftime("%a, %d %b %Y %H:%M", gmtime)
            case constants.DISPLAY_ROLE, 1:
                return commit.hexsha
            case constants.DISPLAY_ROLE, 2:
                return str(commit.author)
            case constants.DISPLAY_ROLE, 3:
                summary = commit.summary
                return summary.decode() if isinstance(summary, bytes) else summary
            case constants.USER_ROLE, _:
                return commit
        return None

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, git.Commit)

    def _fetch_object_children(
        self, item: GitPythonTreeModel.TreeItem
    ) -> list[GitPythonTreeModel.TreeItem]:
        return [self.TreeItem(obj=i) for i in item.obj.parents]

    def _has_children(self, item: GitPythonTreeModel.TreeItem) -> bool:
        return len(item.obj.parents) > 0


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    view = widgets.TreeView()
    view.setRootIsDecorated(True)
    p = pathlib.Path.cwd()
    model = GitPythonCommitTreeModel(p)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("editor")
    view.resize(1000, 1000)
    view.show()
    with app.debug_mode():
        app.exec()
