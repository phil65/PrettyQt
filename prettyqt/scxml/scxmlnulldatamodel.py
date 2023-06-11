from __future__ import annotations

from prettyqt import scxml
from prettyqt.qt import QtScxml


class ScxmlNullDataModel(
    scxml.scxmldatamodel.ScxmlDataModelMixin, QtScxml.QScxmlNullDataModel
):
    pass
