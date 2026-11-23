from __future__ import annotations

from collections.abc import Sequence
import logging
from typing import Any, ClassVar

from prettyqt import constants, core, itemmodels
from prettyqt.utils import bidict


logger = logging.getLogger(__name__)


class ModelIndexModel(itemmodels.ListMixin, core.AbstractTableModel):
    """Table model for displaying a the data of a list of ModelIndexes.

    ### Example:
    ```py
    # get indexes from some random model
    my_model = ParentClassTreeModel(widgets.QWidget, show_mro=True)
    indexes = list(my_model.iter_tree(fetch_more=True))
    model = ModelIndexModel(indexes=indexes)
    ```
    """

    SUPPORTS = Sequence[core.QModelIndex]
    ID = "modelindex"
    FIXED_HEADER: ClassVar = ["Path", "Row", "Column", "Flags"]

    def __init__(
        self,
        indexes: list[core.ModelIndex],
        **kwargs,
    ):
        self._use_model_roles = False
        super().__init__(items=indexes, **kwargs)
        self._update_columns()

    def _update_columns(self):
        if self.items and self._use_model_roles:
            # we assume here that all indexes have some model.
            model = self.items[0].model()
            roles = bidict({i: v.data().decode() for i, v in model.roleNames().items()})
            self.role_mapping = roles.inverse
            self.role_headers = list(roles.values())
        else:
            self.role_mapping = {
                f"{k.capitalize()} role": v for k, v in constants.ITEM_DATA_ROLE.items()
            }
            self.role_headers = list(self.role_mapping.keys())

    def setup_delegates(self, view):
        for i, v in enumerate(self.role_mapping.values(), start=len(self.FIXED_HEADER)):
            view.set_delegate("editor", column=i, data_role=v)

    @property
    def headers(self):
        return self.FIXED_HEADER + self.role_headers

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (core.ModelIndex(), *_):
                return True
            case _:
                return False

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self.headers)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE if section < len(
                self.headers
            ):
                return self.headers[section]
            case constants.VERTICAL, constants.DISPLAY_ROLE:
                return str(section)
        return None

    def _get_column_role(self, column: int) -> constants.ItemDataRole | None:
        if column < len(self.FIXED_HEADER):
            return None
        return self.role_mapping[self.headers[column]]

    def data(  # noqa: PLR0911
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        idx = self.items[index.row()]
        col_role = self._get_column_role(index.column())
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                pieces = self.get_index_key(idx, include_column=True)
                return " / ".join(str(i) for i in pieces)
            case constants.DISPLAY_ROLE, 1:
                return str(idx.row())
            case constants.DISPLAY_ROLE, 2:
                return str(idx.column())
            case constants.DISPLAY_ROLE, 3:
                return " / ".join(constants.ITEM_FLAG.get_list(idx.flags()))
            case _, _ if col_role is None:
                return None
            case constants.DISPLAY_ROLE, _:
                return repr(idx.data(col_role))
            case constants.EDIT_ROLE, _:
                return idx.data(col_role)
            case _ if role == col_role:
                # delegates may be set up with data_role=col_role
                return idx.data(col_role)
        return None

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return False
        col_role = self._get_column_role(index.column())
        if col_role is None or role not in (constants.EDIT_ROLE, col_role):
            return False
        idx = self.items[index.row()]
        if not idx.model().setData(idx, value, col_role):
            return False
        self.update_row(index.row())
        return True

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        flags = super().flags(index)
        if not index.isValid() or self._get_column_role(index.column()) is None:
            return flags
        return flags | constants.IS_EDITABLE

    def set_use_model_roles(self, value: bool):
        with self.reset_model():
            self._use_model_roles = value
            self._update_columns()

    def is_using_model_roles(self) -> bool:
        return self._use_model_roles

    use_model_roles = core.Property(
        bool,
        is_using_model_roles,
        set_use_model_roles,
        doc="Whether to use model.roleNames() for the columns.",
    )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    with app.debug_mode():
        view = widgets.TableView()
        my_model = itemmodels.ParentClassTreeModel(widgets.QWidget, show_mro=True)
        indexes = list(my_model.iter_tree(fetch_more=True))
        model = ModelIndexModel(indexes=indexes, parent=view)
        for i, v in enumerate(model.role_mapping.values(), start=len(model.FIXED_HEADER)):
            view.set_delegate("editor", column=i, role=v)
        # view.set_delegate("editor")
        view.set_model(model)
        view.set_selection_behavior("rows")
        view.set_edit_triggers("all")
        view.show()
        view.resize(1000, 1000)
        app.exec()
