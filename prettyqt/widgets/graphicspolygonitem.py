from qtpy import QtWidgets, QtCore

from prettyqt import widgets, gui
from prettyqt.utils import bidict, InvalidParamError


FILL_RULES = bidict(odd_even=QtCore.Qt.OddEvenFill, winding=QtCore.Qt.WindingFill)

QtWidgets.QGraphicsPolygonItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsPolygonItem(QtWidgets.QGraphicsPolygonItem):
    def get_polygon(self):
        return gui.PolygonF(self.polygon())

    def serialize_fields(self):
        return dict(polygon=self.get_polygon(), fill_rule=self.get_fill_rule())

    def set_fill_rule(self, rule: str):
        if rule not in FILL_RULES:
            raise InvalidParamError(rule, FILL_RULES)
        self.setFillRule(FILL_RULES[rule])

    def get_fill_rule(self):
        return FILL_RULES.inv[self.fillRule()]
