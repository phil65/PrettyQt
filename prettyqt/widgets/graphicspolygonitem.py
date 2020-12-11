from typing import Literal

from qtpy import QtWidgets, QtCore

from prettyqt import widgets, gui
from prettyqt.utils import bidict, InvalidParamError


FILL_RULE = bidict(odd_even=QtCore.Qt.OddEvenFill, winding=QtCore.Qt.WindingFill)

FillRuleStr = Literal["odd_even", "winding"]


QtWidgets.QGraphicsPolygonItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsPolygonItem(QtWidgets.QGraphicsPolygonItem):
    def get_polygon(self) -> gui.PolygonF:
        return gui.PolygonF(self.polygon())

    def serialize_fields(self):
        return dict(polygon=self.get_polygon(), fill_rule=self.get_fill_rule())

    def set_fill_rule(self, rule: FillRuleStr):
        if rule not in FILL_RULE:
            raise InvalidParamError(rule, FILL_RULE)
        self.setFillRule(FILL_RULE[rule])

    def get_fill_rule(self) -> FillRuleStr:
        return FILL_RULE.inverse[self.fillRule()]
