from __future__ import annotations

from collections.abc import Sequence
import dataclasses
import logging

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtWidgets

logger = logging.getLogger(__name__)


class DataClassModel(core.AbstractTableModel):
    def __init__(self, items: Sequence[QtWidgets.QWidget], **kwargs):
        super().__init__(**kwargs)
        self.items = items
        klasses = [type(i) for i in items]
        mro_lists = [set(klass.mro()) for klass in klasses]
        self.Class = set.intersection(*mro_lists).pop()
        logger.debug(f"{type(self).__name__}: found common ancestor {self.Class}")
        self.fields = list(dataclasses.fields(self.Class))
        self.fields.sort(key=lambda x: x.name)

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
                return getattr(instance, field.name)
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

    def flags(self, index):
        return (
            super().flags(index)
            if self.Class.__dataclass_params__.frozen
            else (super().flags(index) | constants.IS_EDITABLE)
        )


if __name__ == "__main__":
    from prettyqt import widgets

    @dataclasses.dataclass
    class BaseSetting:
        name: str
        label: str
        description: str
        requires_restart: bool = False

    @dataclasses.dataclass
    class SelectionSetting(BaseSetting):
        options: list[str] | None = None
        minimum: float = 0.0
        maximum: float = 0.0
        pattern: str = ""
        requires_restart: bool = False

    app_style = SelectionSetting(
        name="app_style",
        label="App style",
        description="Some longer text",
        options=[],
        requires_restart=True,
    )
    app = widgets.app()
    items = [BaseSetting(name="test", label="some label", description="jhaj"), app_style]
    klasses = [type(i) for i in items]
    # mro_lists = [set(klass.mro()) for klass in klasses]
    # print(mro_lists)
    # common_ancestor = set.intersection(*mro_lists).pop()
    # print(common_ancestor)
    view = widgets.TableView()
    view.set_icon("mdi.folder")
    model = DataClassModel(items, parent=view)
    view.set_model(model)
    view.setEditTriggers(view.EditTrigger.AllEditTriggers)
    view.set_delegate("variant")
    view.resize(1000, 1000)
    with app.debug_mode():
        view.show()
        app.main_loop()