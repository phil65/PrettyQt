from __future__ import annotations

from prettyqt import scxml


class ScxmlNullDataModel(
    scxml.scxmldatamodel.ScxmlDataModelMixin, scxml.QScxmlNullDataModel
):
    pass
