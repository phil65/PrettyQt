from prettyqt import constants, core, custom_models


class Root:
    def __init__(self, name="Root", children=None):
        self.children = children if children else []
        self.name = name


class NestedModel(  # type: ignore
    custom_models.ListMixin, custom_models.ModelMixin, core.AbstractItemModel
):

    DEFAULT_FLAGS = (
        constants.DRAG_ENABLED  # type: ignore
        | constants.IS_ENABLED
        | constants.IS_SELECTABLE
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = Root()
        self.items = self.root.children

    def flags(self, index):
        if not index.isValid():
            return constants.NO_FLAGS
        if index.column() in self.SET_DATA:
            return self.DEFAULT_FLAGS | constants.IS_EDITABLE
        return self.DEFAULT_FLAGS

    def rowCount(self, parent=core.ModelIndex()) -> int:

        if parent.column() > 0:
            return 0
        if not parent.isValid():
            return len(self.items)
        return len(parent.internalPointer().children)

    def index(self, row, column, parent):

        if not self.hasIndex(row, column, parent):
            return core.ModelIndex()

        parent_item = parent.internalPointer()
        if not parent_item:
            parent_item = self.root

        return self.createIndex(row, column, parent_item.children[row])

    def parent(self, index):

        if not index.isValid():
            return core.ModelIndex()

        item = index.internalPointer()
        if not item:
            return core.ModelIndex()

        if item.parent in [self.root, None]:
            return core.ModelIndex()

        return self.createIndex(item.parent.row(), 0, item.parent)

    def data_by_index(self, index):
        return index.internalPointer()

    def json(self, root=None) -> dict:
        """Serialise model as JSON-compliant dictionary.

        Arguments:
            root (JsonTreeItem, optional): Serialise from here
                defaults to the the top-level item

        Returns:
            model as dict
        """
        root = root if root else self.root
        return root.as_json()
