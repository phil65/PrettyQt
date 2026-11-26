from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtScxml


if TYPE_CHECKING:
    _ScxmlDataModelBase = QtScxml.QScxmlDataModel
else:
    _ScxmlDataModelBase = object


class ScxmlDataModelMixin(core.ObjectMixin, _ScxmlDataModelBase):
    pass


class ScxmlDataModel(ScxmlDataModelMixin, QtScxml.QScxmlDataModel):
    """The data model base class for a Qt SCXML state machine."""
