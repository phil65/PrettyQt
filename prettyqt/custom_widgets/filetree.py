from prettyqt import widgets


class FileTree(widgets.TreeView):
    def __init__(self, filters: list[str] | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRootIsDecorated(True)
        self.h_header.set_resize_mode("resize_to_contents")
        self.setup_dragdrop_move()

        model = widgets.FileSystemModel()
        model.use_custom_icons(False)
        model.resolve_sym_links(False)
        model.set_root_path("C:/")
        if filters:
            model.set_name_filters(filters, hide=False)
        self.set_model(model)
        self.expanded_ids = []

    def get_expanded_state(self) -> list[str]:
        self.expanded_ids = []
        for i in range(self.model().rowCount()):
            self.save_expanded_on_level(self.model().index(i, 0))
        return self.expanded_ids

    def set_expanded_state(self, state):
        self.expanded_ids = state
        with self.updates_off():
            for i in range(self.model().rowCount()):
                self.restore_expanded_on_level(self.model().index(i, 0))

    def save_expanded_on_level(self, index):
        if not self.isExpanded(index):
            return None
        if index.isValid():
            path = str(self.model().get_file_path(index))
            self.expanded_ids.append(path)
        for i in range(self.model().rowCount(index)):
            val = self.model().index(i, 0, index)
            self.save_expanded_on_level(val)

    def restore_expanded_on_level(self, index):
        path = self.model().get_file_path(index)
        if str(path) not in self.expanded_ids:
            return None
        self.setExpanded(index, True)
        if not self.model().hasChildren(index):
            return None
        for it in path.iterdir():
            child_index = self.model().index(str(path / it))
            self.restore_expanded_on_level(child_index)


if __name__ == "__main__":
    app = widgets.app()
    w = FileTree()
    w.show()
    app.main_loop()
