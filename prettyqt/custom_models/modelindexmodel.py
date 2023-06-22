from __future__ import annotations

import logging
from typing import Any

from prettyqt import constants, core, custom_models
from prettyqt.utils import bidict

logger = logging.getLogger(__name__)


class ModelIndexModel(custom_models.ListMixin, core.AbstractTableModel):
    ID = "modelindex"
    FIXED_HEADER = ["Path", "Column", "Row", "Flags"]

    def __init__(
        self,
        indexes: list[core.ModelIndex],
        use_model_roles: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.items = indexes
        self._use_model_roles = use_model_roles
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
            view.set_delegate("variant", column=i, data_role=v)

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

    def columnCount(self, parent=None) -> int:
        return len(self.headers)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self.headers[section]
            case constants.VERTICAL, constants.DISPLAY_ROLE:
                return str(section)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        idx = self.items[index.row()]
        header = self.headers[index.column()]
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                #  pieces = self.get_breadcrumbs_path()
                pieces = self.get_index_key(idx)
                return " / ".join(str(i) for i in pieces)
            case constants.DISPLAY_ROLE, 1:
                return idx.column()
            case constants.DISPLAY_ROLE, 2:
                return idx.row()
            case constants.DISPLAY_ROLE, 3:
                roles = constants.ITEM_FLAG.get_list(idx.flags())
                return " / ".join(roles)
            case constants.DISPLAY_ROLE, _:
                role = self.role_mapping[header]
                return repr(idx.data(role))
            case _ as role, _:
                # print(self.headers[column], role)
                return idx.data(role)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        idx = self.items[index.row()]
        idx.model().setData(idx, value, role)
        self.update_row(index.row())
        return True

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        return super().flags(index) | constants.IS_EDITABLE
        # idx = self.items[index.row()]
        # return idx.flags()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    with app.debug_mode():
        view = widgets.TableView()
        test = custom_models.ParentClassTreeModel(widgets.PlainTextEdit, parent=view)
        test.prefetch_tree()
        indexes = list(test.iter_tree())
        model = ModelIndexModel(indexes=indexes, parent=view)
        for i, v in enumerate(model.role_mapping.values(), start=len(model.FIXED_HEADER)):
            view.set_delegate("variant", column=i, data_role=v)
        # view.set_delegate("variant")
        view.set_model(model)
        view.set_selection_behavior("rows")
        view.set_edit_triggers("all")
        view.show()
        view.resize(1000, 1000)
        app.exec()
