from __future__ import annotations

import logging
import os
import pathlib

from prettyqt import core, widgets


logger = logging.getLogger(__name__)


class FileTree(widgets.TreeView):
    def __init__(self, *args, filters: list[str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRootIsDecorated(True)
        self.h_header.set_resize_mode("resize_to_contents")
        self.setup_dragdrop_move()

        model = widgets.FileSystemModel()
        model.resolve_sym_links(False)
        model.set_root_path("C:/")
        if filters:
            model.set_name_filters(filters, hide=False)
        self.set_model(model)
        self.expanded_ids = []

    def get_expanded_state(self) -> list[str]:
        self.expanded_ids = []
        for i in range(self.model().rowCount()):
            self._save_expanded_on_level(self.model().index(i, 0))
        return self.expanded_ids

    def set_expanded_state(self, state: list[str]):
        self.expanded_ids = state
        with self.updates_off():
            for i in range(self.model().rowCount()):
                self._restore_expanded_on_level(self.model().index(i, 0))

    def _save_expanded_on_level(self, index: core.ModelIndex):
        if not self.isExpanded(index):
            return None
        model = self.model()
        if index.isValid():
            path = model.data(index, model.FilePathRole)
            self.expanded_ids.append(path)
        for i in range(model.rowCount(index)):
            val = model.index(i, 0, index)
            self._save_expanded_on_level(val)

    def _restore_expanded_on_level(self, index: core.ModelIndex):
        model = self.model()
        path = model.data(index, model.FilePathRole)
        if path not in self.expanded_ids:
            return None
        self.setExpanded(index, True)
        if not model.hasChildren(index):
            return None
        path = pathlib.Path(path)
        for it in path.iterdir():
            child_index = model.index(str(path / it))
            self._restore_expanded_on_level(child_index)


class BreadCrumbsToolBar(widgets.ToolBar):
    path_clicked = core.Signal(pathlib.Path)

    def set_breadcrumbs(self, path: os.PathLike):
        self.clear()
        path = pathlib.Path(path)
        logger.info(f"Setting breadrumbs to {path}")
        if path.parents:
            action = self.add_action(
                text=str(path.parents[-1]), triggered=self._on_button_clicked
            )
            action.setData(path.parents[-1])
        for p in reversed(path.parents[:-1]):
            action = self.add_action(text=p.name, triggered=self._on_button_clicked)
            action.setData(p)
        if path.is_dir():
            action = self.add_action(text=path.name, triggered=self._on_button_clicked)
            action.setData(path)

    def _on_button_clicked(self, button):
        action = self.sender()
        path = action.data()
        self.path_clicked.emit(path)


class FileExplorer(widgets.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_edit = widgets.LineEdit()
        self._file_tree = FileTree(self)
        self.tool_bar = BreadCrumbsToolBar(self)

        self._file_tree.selectionModel().currentChanged.connect(self._on_current_changed)
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

    def _update_root(self, path: os.PathLike):
        if pathlib.Path(path).exists():
            self._file_tree.setRoot(os.fspath(path))


if __name__ == "__main__":
    app = widgets.app()
    w = FileExplorer()
    w.show()
    app.main_loop()
