from __future__ import annotations

import logging
import os
import pathlib
from typing import TYPE_CHECKING

from prettyqt import core, widgets
from prettyqt.gui.action import Action


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class FileTree(widgets.TreeView):
    def __init__(self, *args, filters: list[str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRootIsDecorated(True)
        self.setup_dragdrop_move()
        self._model = widgets.FileSystemModel()
        self._model.resolve_sym_links(False)
        if filters:
            self._model.set_name_filters(filters, hide=False)
        self.set_model(self._model)
        self._expanded_ids: list[str] = []

    def get_expanded_state(self, root_index: core.ModelIndex | None = None) -> list[str]:
        """Get a list of all expanded paths.

        Can be used to re-expand to the same state.
        """
        root = root_index or self.rootIndex()
        model = self.model()
        self._expanded_ids = []

        def _save_expanded_on_level(index: core.ModelIndex):
            if not self.isExpanded(index):
                return
            if index.isValid():
                path = model.data(index, self._model.Roles.FilePathRole)
                self._expanded_ids.append(path)
            for i in range(model.rowCount(index)):
                val = model.index(i, 0, index)
                _save_expanded_on_level(val)

        for i in range(model.rowCount(root)):
            _save_expanded_on_level(model.index(i, 0, root))
        return self._expanded_ids

    def set_expanded_state(
        self, state: list[str], root_index: core.ModelIndex | None = None
    ):
        """Set all indexes which correspond to given paths to expanded."""
        root = root_index or self.rootIndex()
        model = self.model()
        self._expanded_ids = state

        def _restore_expanded_on_level(index: core.ModelIndex):
            model = self._model
            path = model.data(index, model.Roles.FilePathRole)
            if path not in self._expanded_ids:
                return
            self.setExpanded(index, True)
            if not model.hasChildren(index):
                return
            path = pathlib.Path(path)
            for it in path.iterdir():
                child_index = model.index(str(path / it))
                _restore_expanded_on_level(child_index)

        with self.updates_off():
            for i in range(model.rowCount(root)):
                _restore_expanded_on_level(model.index(i, 0))

    def set_root_path(self, path: datatypes.PathType):
        """Set tree rootpath to given path."""
        path = os.fspath(path)
        self._model.set_root_path(path)
        index = self._model.index(path)
        self.setRootIndex(index)


class BreadCrumbsToolBar(widgets.ToolBar):
    path_clicked = core.Signal(pathlib.Path)

    def set_breadcrumbs(self, path: datatypes.PathType):
        self.clear()
        path = pathlib.Path(path)
        logger.info("Setting breadrumbs to %s", path)
        if path.parents:
            action = self.add_action(
                text=str(path.parents[-1]), callback=self._on_button_clicked
            )
            action.setData(path.parents[-1])
        for p in reversed(path.parents[:-1]):
            action = self.add_action(text=p.name, callback=self._on_button_clicked)
            action.setData(p)
        if path.is_dir():
            action = self.add_action(text=path.name, callback=self._on_button_clicked)
            action.setData(path)

    def _on_button_clicked(self, button):
        if action := self.get_sender(Action):
            path = action.data()
            self.path_clicked.emit(path)


class FileExplorer(widgets.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_edit = widgets.LineEdit()
        self._file_tree = FileTree(self)
        self.tool_bar = BreadCrumbsToolBar(self)

        self._file_tree.selectionModel().currentRowChanged.connect(
            self._on_current_changed
        )
        self.tool_bar.path_clicked.connect(self._on_breadcrumbs_clicked)
        self._file_edit.value_changed.connect(self._update_root)

        with widgets.VBoxLayout(self) as layout:
            layout.addWidget(self.tool_bar)
            # layout.addWidget(self._file_edit)
            layout.addWidget(self._file_tree)
        # self._update_root(curpath)

    def _on_breadcrumbs_clicked(self, path: pathlib.Path):
        index = self._file_tree.model().index(str(path))
        self._file_tree.set_current_index(index)

    def _on_current_changed(self, new, _):
        if (model := new.model()) is not None:
            path = new.data(model.Roles.FilePathRole)
            self.tool_bar.set_breadcrumbs(path)

    def _update_root(self, path: os.PathLike[str]):
        if pathlib.Path(path).exists():
            self._file_tree.set_root_path(os.fspath(path))


if __name__ == "__main__":
    app = widgets.app()
    w = FileTree()
    w.set_root_path("C:/")
    w.show()
    app.exec()
    print(w.get_expanded_state())
