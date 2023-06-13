from __future__ import annotations

from collections.abc import Sequence
import collections
import functools
import pydantic
import contextlib
import logging
from operator import and_

from prettyqt import constants, core
from prettyqt.qt import QtCore

logger = logging.getLogger(__name__)


def lca_type(classes: list[type]) -> type:
    return next(
        iter(functools.reduce(and_, (collections.Counter(cls.mro()) for cls in classes)))
    )


class BaseDataclassModel(core.AbstractTableModel):
    # Apart from attrs.fields / dataclasses.fields, only difference to
    # DataclassModel is flags method
    def __init__(self, items: Sequence, **kwargs):
        super().__init__(**kwargs)
        self.items = items
        klasses = [type(i) for i in items]
        self.Class = lca_type(klasses)
        logger.debug(f"{type(self).__name__}: found common ancestor {self.Class}")
        self.fields = self.get_fields()
        self.fields.sort(key=lambda x: x.name)

    def get_fields(self):
        return NotImplemented

    def columnCount(self, parent=None):
        return len(self.fields)

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole,
    ) -> str | None:
        match orientation, role, section:
            case constants.VERTICAL, constants.DISPLAY_ROLE, _:
                instance = self.items[section]
                return type(instance).__name__
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self.fields[section].name

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        field = self.fields[index.column()]
        instance = self.items[index.row()]
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                return repr(getattr(instance, field.name))
            case constants.USER_ROLE:
                return getattr(instance, field.name)

    def setData(self, index, value, role=constants.DISPLAY_ROLE):
        field = self.fields[index.column()]
        instance = self.items[index.row()]
        match role:
            case constants.USER_ROLE:
                with self.reset_model():
                    setattr(instance, field.name, value)
                return True
        return False

    def rowCount(self, parent=None):
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self.items)

    def flags(self, parent=None):
        """Override.

        BaseClass implementation just tries to set attribute with same value to test
        if field is writable.
        """
        if not parent.isValid():
            return super().flags(parent)
        parent = parent or core.ModelIndex()
        field = self.fields[parent.column()]
        instance = self.items[parent.row()]
        # need to cover not parent.isValid()?
        val = getattr(instance, field.name)
        with contextlib.suppress(Exception):
            setattr(instance, field.name, val)
            return super().flags(parent) | constants.IS_EDITABLE
        return super().flags(parent)


if __name__ == "__main__":
    from prettyqt import widgets

    class BaseSetting(pydantic.BaseModel):
        name: str
        label: str
        description: str
        requires_restart: bool = False
        options: list[str] | None = None
        minimum: float = 0.0
        maximum: float = 0.0
        pattern: str = ""
        requires_restart: bool = False

    class SelectionSetting(BaseSetting):
        options: list[str] | None = None
        minimum: float = 0.0
        maximum: float = 0.0
        pattern: str = ""
        requires_restart: bool = False

    app_style = BaseSetting(
        name="app_style",
        label="App style",
        description="Some longer text",
        options=[],
        requires_restart=True,
    )
    app = widgets.app()
    with app.debug_mode():
        items = [
            BaseSetting(name=f"test{i}", label="some label", description="jhaj")
            for i in range(5)
        ]
        view = widgets.TableView()
        view.set_icon("mdi.folder")
        model = BaseDataclassModel(items, parent=view)
        view.set_model(model)
        view.setEditTriggers(view.EditTrigger.AllEditTriggers)
        view.set_delegate("variant")
        view.resize(1000, 1000)
        view.show()
        app.main_loop()
