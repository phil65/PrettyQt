from typing import List, Optional, Union, Tuple

from qtpy import QtWidgets, QtGui, QtCore

from prettyqt import core, widgets, gui
from prettyqt.utils import InvalidParamError, bidict


ITEM_SELECTION_MODES = bidict(
    contains_shape=QtCore.Qt.ContainsItemShape,
    intersects_shape=QtCore.Qt.IntersectsItemShape,
    contains_bounding_rect=QtCore.Qt.ContainsItemBoundingRect,
    intersects_bounding_rect=QtCore.Qt.IntersectsItemBoundingRect,
)

SCENE_LAYERS = bidict(
    item=QtWidgets.QGraphicsScene.ItemLayer,
    background=QtWidgets.QGraphicsScene.BackgroundLayer,
    foreground=QtWidgets.QGraphicsScene.ForegroundLayer,
    all=QtWidgets.QGraphicsScene.AllLayers,
)

ITEM_INDEX_METHODS = bidict(
    bsp_tree=QtWidgets.QGraphicsScene.BspTreeIndex, none=QtWidgets.QGraphicsScene.NoIndex
)

QtWidgets.QGraphicsScene.__bases__ = (core.Object,)


class GraphicsScene(QtWidgets.QGraphicsScene):
    def serialize_fields(self):
        return dict(
            items=self.items(),
            background_brush=gui.Brush(self.backgroundBrush()),
            foreground_brush=gui.Brush(self.foregroundBrush()),
            item_index_method=self.get_item_index_method(),
            minimum_render_size=self.minimumRenderSize(),
            palette=gui.Palette(self.palette()),
            bsp_tree_depth=self.bspTreeDepth(),
            focus_on_touch=self.focusOnTouch(),
            sticky_focus=self.stickyFocus(),
            scene_rect=core.RectF(self.sceneRect()),
            font=gui.Font(self.font()),
        )

    def __getitem__(self, index: int):
        return self.items()[index]

    def add(self, item) -> QtWidgets.QGraphicsItem:
        if isinstance(item, QtWidgets.QGraphicsItem):
            self.addItem(item)
            return item
        elif isinstance(item, QtGui.QPixmap):
            return self.add_pixmap(item)
        elif isinstance(item, QtGui.PainterPath):
            return self.add_path(item)
        elif isinstance(item, QtGui.QPolygonF):
            return self.add_polygon(item)
        elif isinstance(item, QtCore.QRectF):
            return self.add_rect(item)
        elif isinstance(item, QtCore.QLine):
            return self.add_line(item)
        elif isinstance(item, str):
            return self.add_text(item)
        elif isinstance(item, QtWidgets.QWidget):
            return self.add_widget(item)

    def add_pixmap(self, pixmap: QtGui.QPixmap) -> widgets.GraphicsPixmapItem:
        g_item = widgets.GraphicsPixmapItem()
        g_item.setPixmap(pixmap)
        self.addItem(g_item)
        return g_item

    def add_polygon(
        self,
        polygon: QtGui.QPolygonF,
        pen: Optional[QtGui.QPen] = None,
        brush: Optional[QtGui.QBrush] = None,
    ) -> widgets.GraphicsPolygonItem:
        if isinstance(polygon, QtGui.QPolygon):
            polygon = gui.PolygonF(polygon)
        g_item = widgets.GraphicsPolygonItem()
        g_item.setPolygon(polygon)
        if brush is not None:
            g_item.setBrush(brush)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_path(
        self,
        path: QtGui.QPainterPath,
        pen: Optional[QtGui.QPen] = None,
        brush: Optional[QtGui.QBrush] = None,
    ) -> widgets.GraphicsPathItem:
        g_item = widgets.GraphicsPathItem()
        g_item.setPath(path)
        if brush is not None:
            g_item.setBrush(brush)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_rect(
        self,
        rect: Union[QtCore.QRectF, QtCore.QRect, Tuple[float, float, float, float]],
        pen: Optional[QtGui.QPen] = None,
        brush: Optional[QtGui.QBrush] = None,
    ) -> widgets.GraphicsRectItem:
        if isinstance(rect, QtCore.QRect):
            rect = core.RectF(rect)
        elif isinstance(rect, tuple):
            rect = core.RectF(*rect)
        g_item = widgets.GraphicsRectItem()
        g_item.setRect(rect)
        if brush is not None:
            g_item.setBrush(brush)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_line(
        self,
        line: Union[QtCore.QLineF, QtCore.QLine, Tuple[float, float, float, float]],
        pen: Optional[QtGui.QPen] = None,
    ) -> widgets.GraphicsLineItem:
        if isinstance(line, QtCore.QLine):
            line = core.LineF(line)
        elif isinstance(line, tuple):
            line = core.LineF(*line)
        g_item = widgets.GraphicsLineItem()
        g_item.setLine(line)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_ellipse(
        self,
        ellipse: Union[QtCore.QRectF, QtCore.QRect, Tuple[float, float, float, float]],
        pen: Optional[QtGui.QPen] = None,
        brush: Optional[QtGui.QBrush] = None,
    ) -> widgets.GraphicsEllipseItem:
        if isinstance(ellipse, QtCore.QRect):
            ellipse = core.RectF(ellipse)
        elif isinstance(ellipse, tuple):
            ellipse = core.RectF(*ellipse)
        g_item = widgets.GraphicsEllipseItem()
        g_item.setRect(ellipse)
        if brush is not None:
            g_item.setBrush(brush)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_text(
        self, text: str, font: Optional[QtGui.QFont] = None
    ) -> widgets.GraphicsTextItem:
        g_item = widgets.GraphicsTextItem()
        g_item.setPlainText(text)
        if font is not None:
            g_item.setFont(font)
        self.addItem(g_item)
        return g_item

    def add_simple_text(
        self, text: str, font: Optional[QtGui.QFont] = None
    ) -> widgets.GraphicsSimpleTextItem:
        g_item = widgets.GraphicsSimpleTextItem()
        g_item.setText(text)
        if font is not None:
            g_item.setFont(font)
        self.addItem(g_item)
        return g_item

    def add_widget(self, widget: QtWidgets.QWidget) -> widgets.GraphicsProxyWidget:
        g_item = widgets.GraphicsProxyWidget()
        g_item.setWidget(widget)
        self.addItem(g_item)
        return g_item

    def colliding_items(
        self, item: QtWidgets.QGraphicsItem, mode: str = "intersects_shape"
    ) -> List[QtWidgets.QGraphicsItem]:
        if mode not in ITEM_SELECTION_MODES:
            raise InvalidParamError(mode, ITEM_SELECTION_MODES)
        return self.collidingItems(item, ITEM_SELECTION_MODES[mode])

    def add_item_group(
        self, *items: QtWidgets.QGraphicsItem
    ) -> widgets.GraphicsItemGroup:
        group = widgets.GraphicsItemGroup()
        for item in items:
            group.addToGroup(item)
        return group

    def set_item_index_method(self, method: str):
        """Set item index method.

        possible values are "bsp_tree", "none"

        Args:
            method: item index method to use

        Raises:
            InvalidParamError: invalid item index method
        """
        if method not in ITEM_INDEX_METHODS:
            raise InvalidParamError(method, ITEM_INDEX_METHODS)
        self.setItemIndexMethod(ITEM_INDEX_METHODS[method])

    def get_item_index_method(self) -> str:
        """Return item index method.

        possible values are "bsp_tree", "none"

        Returns:
            item index method
        """
        return ITEM_INDEX_METHODS.inv[self.itemIndexMethod()]


if __name__ == "__main__":
    app = widgets.app()
    scene = GraphicsScene()
    scene.add_line(core.Line(0, 0, 10, 10))
    scene.show()
    app.main_loop()
    scene.show()
