from __future__ import annotations

import pathlib

from prettyqt import widgets


class FileTree(widgets.TreeView):
    def __init__(self, filters: list[str] | None = None, *args, **kwargs):
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

    def set_expanded_state(self, state):
        self.expanded_ids = state
        with self.updates_off():
            for i in range(self.model().rowCount()):
                self._restore_expanded_on_level(self.model().index(i, 0))

    def _save_expanded_on_level(self, index):
        if not self.isExpanded(index):
            return None
        if index.isValid():
            path = self.model().data(index, self.model().FilePathRole)
            self.expanded_ids.append(path)
        for i in range(self.model().rowCount(index)):
            val = self.model().index(i, 0, index)
            self._save_expanded_on_level(val)

    def _restore_expanded_on_level(self, index):
        path = self.model().data(index, self.model().FilePathRole)
        if path not in self.expanded_ids:
            return None
        self.setExpanded(index, True)
        if not self.model().hasChildren(index):
            return None
        path = pathlib.Path(path)
        for it in path.iterdir():
            child_index = self.model().index(str(path / it))
            self._restore_expanded_on_level(child_index)


if __name__ == "__main__":
    app = widgets.app()
    w = FileTree()
    w.show()
    app.main_loop()
