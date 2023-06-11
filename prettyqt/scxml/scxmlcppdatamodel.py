from __future__ import annotations

from prettyqt import scxml
from prettyqt.qt import QtScxml


class ScxmlCppDataModel(
    scxml.scxmldatamodel.ScxmlDataModelMixin, QtScxml.QScxmlCppDataModel
):
    pass
