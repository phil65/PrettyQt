from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


SCENE_LAYER = bidict(
    item=QtWidgets.QGraphicsScene.SceneLayer.ItemLayer,
    background=QtWidgets.QGraphicsScene.SceneLayer.BackgroundLayer,
    foreground=QtWidgets.QGraphicsScene.SceneLayer.ForegroundLayer,
    all=QtWidgets.QGraphicsScene.SceneLayer.AllLayers,
)

SceneLayerStr = Literal["item", "background", "foreground", "all"]

ITEM_INDEX_METHOD = bidict(
    bsp_tree=QtWidgets.QGraphicsScene.ItemIndexMethod.BspTreeIndex,
    none=QtWidgets.QGraphicsScene.ItemIndexMethod.NoIndex,
)

ItemIndexMethodStr = Literal["bsp_tree", "none"]

QtWidgets.QGraphicsScene.__bases__ = (core.Object,)


class GraphicsScene(QtWidgets.QGraphicsScene):
    def serialize_fields(self):
        return dict(
            items=self.items(),
            background_brush=self.get_background_brush(),
            foreground_brush=self.get_foreground_brush(),
            item_index_method=self.get_item_index_method(),
            minimum_render_size=self.minimumRenderSize(),
            palette=self.get_palette(),
            bsp_tree_depth=self.bspTreeDepth(),
            focus_on_touch=self.focusOnTouch(),
            sticky_focus=self.stickyFocus(),
            scene_rect=core.RectF(self.sceneRect()),
            font=self.get_font(),
        )

    def __setitem__(self, state):
        # self.setItem
        self.setBackgroundBrush(state["background_brush"])
        self.setForegroundBrush(state["foreground_brush"])
        self.set_item_index_method(state["item_index_method"])
        self.setMinimumRenderSize(state["minimum_render_size"])
        self.setPalette(state["palette"])
        self.setBspTreeDepth(state["bsp_tree_depth"])
        self.setFocusOnTouchRelease(state["focus_on_touch"])
        self.setStickyFocus(state["focus_on_touch"])
        self.setSceneRect(state["scene_rect"])
        self.setFont(state["font"])

    def __getitem__(self, index: int) -> QtWidgets.QGraphicsItem:
        return self.items()[index]

    def get_palette(self) -> gui.Palette:
        return gui.Palette(self.palette())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_background_brush(self) -> gui.Brush:
        return gui.Brush(self.backgroundBrush())

    def get_foreground_brush(self) -> gui.Brush:
        return gui.Brush(self.foregroundBrush())

    def add(self, item) -> QtWidgets.QGraphicsItem:
        if isinstance(item, QtWidgets.QGraphicsItem):
            self.addItem(item)
            return item
        elif isinstance(item, QtGui.QPixmap):
            return self.add_pixmap(item)
        elif isinstance(item, QtGui.QPainterPath):
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
        else:
            raise TypeError(item)

    def add_pixmap(self, pixmap: QtGui.QPixmap) -> widgets.GraphicsPixmapItem:
        g_item = widgets.GraphicsPixmapItem()
        g_item.setPixmap(pixmap)
        self.addItem(g_item)
        return g_item

    def add_polygon(
        self,
        polygon: QtGui.QPolygonF | QtGui.QPolygon,
        pen: QtGui.QPen | None = None,
        brush: QtGui.QBrush | None = None,
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
        pen: QtGui.QPen | None = None,
        brush: QtGui.QBrush | None = None,
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
        rect: types.RectType | types.RectFType,
        pen: QtGui.QPen | None = None,
        brush: QtGui.QBrush | None = None,
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
        line: QtCore.QLineF | QtCore.QLine | tuple[float, float, float, float],
        pen: QtGui.QPen | None = None,
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
        ellipse: types.RectType | types.RectFType,
        pen: QtGui.QPen | None = None,
        brush: QtGui.QBrush | None = None,
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
        self, text: str, font: QtGui.QFont | None = None
    ) -> widgets.GraphicsTextItem:
        g_item = widgets.GraphicsTextItem()
        g_item.setPlainText(text)
        if font is not None:
            g_item.setFont(font)
        self.addItem(g_item)
        return g_item

    def add_simple_text(
        self, text: str, font: QtGui.QFont | None = None
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
        self,
        item: QtWidgets.QGraphicsItem,
        mode: constants.ItemSelectionModeStr = "intersects_shape",
    ) -> list[QtWidgets.QGraphicsItem]:
        if mode not in constants.ITEM_SELECTION_MODE:
            raise InvalidParamError(mode, constants.ITEM_SELECTION_MODE)
        return self.collidingItems(item, constants.ITEM_SELECTION_MODE[mode])

    def add_item_group(
        self, *items: QtWidgets.QGraphicsItem
    ) -> widgets.GraphicsItemGroup:
        group = widgets.GraphicsItemGroup()
        for item in items:
            group.addToGroup(item)
        return group

    def set_item_index_method(self, method: ItemIndexMethodStr):
        """Set item index method.

        Args:
            method: item index method to use

        Raises:
            InvalidParamError: invalid item index method
        """
        if method not in ITEM_INDEX_METHOD:
            raise InvalidParamError(method, ITEM_INDEX_METHOD)
        self.setItemIndexMethod(ITEM_INDEX_METHOD[method])

    def get_item_index_method(self) -> ItemIndexMethodStr:
        """Return item index method.

        Returns:
            item index method
        """
        return ITEM_INDEX_METHOD.inverse[self.itemIndexMethod()]


if __name__ == "__main__":
    app = widgets.app()
    scene = GraphicsScene()
    scene.add_line(core.Line(0, 0, 10, 10))
    view = widgets.GraphicsView(scene)
    view.show()
    app.main_loop()
