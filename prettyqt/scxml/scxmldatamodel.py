from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtScxml


class ScxmlDataModelMixin(core.ObjectMixin):
    pass


class ScxmlDataModel(ScxmlDataModelMixin, QtScxml.QScxmlDataModel):
    """The data model base class for a Qt SCXML state machine."""
