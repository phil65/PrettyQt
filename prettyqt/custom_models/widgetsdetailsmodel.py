from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
import inspect
import logging

from prettyqt import constants, core
from prettyqt.qt import QtCore, QtWidgets


logger = logging.getLogger(__name__)


def find_common_ancestor(cls_list):
    mros = [list(inspect.getmro(cls)) for cls in cls_list]
    track = defaultdict(int)
    while mros:
        for mro in mros:
            cur = mro.pop(0)
            track[cur] += 1
            if (
                track[cur] >= len(cls_list)
                and not cur.__name__.endswith("Mixin")
                and cur.__name__.startswith("Q")
            ):
                return cur
            if len(mro) == 0:
                mros.remove(mro)
    raise TypeError("Couldnt find common base class")


class WidgetsDetailsModel(core.AbstractTableModel):
    def __init__(self, items: Sequence[QtWidgets.QWidget], **kwargs):
        super().__init__(**kwargs)
        self.items = items
        common_ancestor = find_common_ancestor([type(i) for i in self.items])
        logger.debug(f"{type(self).__name__}: found common ancester {common_ancestor}")
        self._metaobj = core.MetaObject(common_ancestor.staticMetaObject)

    def columnCount(self, parent=None):
        return widgets.Widget.get_static_metaobject().propertyCount()

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        role: QtCore.Qt.ItemDataRole,
    ) -> str | None:
        match orientation, role, section:
            case constants.VERTICAL, constants.DISPLAY_ROLE, _:
                widget = self.items[section]
                return repr(widget)
            case constants.HORIZONTAL, constants.DISPLAY_ROLE, _:
                return self._metaobj.get_property(section).get_name()

    def data(self, index, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        prop = self._metaobj.get_property(index.column())
        widget = self.items[index.row()]
        match role:
            case constants.DISPLAY_ROLE | constants.EDIT_ROLE:
                return prop.read(widget)
            case constants.USER_ROLE:
                return prop.read(widget)

    def setData(self, index, value, role=constants.DISPLAY_ROLE):
        if not index.isValid():
            return None
        prop = self._metaobj.get_property(index.column())
        widget = self.items[index.row()]
        match role:
            case constants.USER_ROLE:
                prop.write(widget, value)
                self.update_row(index.row())
                return True
        return False

    def rowCount(self, parent=None):
        """Override for AbstractitemModel base method."""
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return 0
        return 0 if parent.isValid() else len(self.items)

    def flags(self, index):
        prop = self._metaobj.get_property(index.column())
        if prop.isWritable():
            return (
                super().flags(index)
                | constants.IS_EDITABLE
                | constants.IS_ENABLED
                | constants.IS_SELECTABLE
            )
        return super().flags(index)


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_delegates import variantdelegate

    app = widgets.app()
    view = widgets.TableView()
    view.set_icon("mdi.folder")
    items = [widgets.RadioButton(), widgets.RadioButton()]
    model = WidgetsDetailsModel(items)
    delegate = variantdelegate.VariantDelegate(parent=view)
    view.set_model(model)
    view.set_selection_behavior("rows")
    view.setEditTriggers(
        view.EditTrigger.DoubleClicked | view.EditTrigger.SelectedClicked
    )
    view.set_delegate(delegate)
    view.resize(500, 300)
    with app.debug_mode():
        view.show()
        app.main_loop()
