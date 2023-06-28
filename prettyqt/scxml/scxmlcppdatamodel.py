from __future__ import annotations

from prettyqt import scxml


class ScxmlCppDataModel(
    scxml.scxmldatamodel.ScxmlDataModelMixin, scxml.QScxmlCppDataModel
):
    pass
