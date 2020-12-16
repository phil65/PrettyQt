from typing import List, Literal

from qtpy import QtCore, QtWidgets

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import InvalidParamError, bidict, helpers, mappers


DRAG_MODE = bidict(
    none=QtWidgets.QGraphicsView.NoDrag,
    scroll_hand=QtWidgets.QGraphicsView.ScrollHandDrag,
    rubber_band=QtWidgets.QGraphicsView.RubberBandDrag,
)

DragModeStr = Literal["none", "scroll_hand", "rubber_band"]

CACHE_MODES = mappers.FlagMap(
    QtWidgets.QGraphicsView.CacheMode,
    none=QtWidgets.QGraphicsView.CacheNone,
    background=QtWidgets.QGraphicsView.CacheBackground,
)

CacheModeStr = Literal["none", "background"]

OPTIMIZATION_FLAGS = bidict(
    dont_clip_painter=QtWidgets.QGraphicsView.DontClipPainter,
    dont_save_painter_state=QtWidgets.QGraphicsView.DontSavePainterState,
    dont_adjust_for_antialiasing=QtWidgets.QGraphicsView.DontAdjustForAntialiasing,
)

VIEWPORT_ANCHOR = bidict(
    none=QtWidgets.QGraphicsView.NoAnchor,
    view_center=QtWidgets.QGraphicsView.AnchorViewCenter,
    under_mouse=QtWidgets.QGraphicsView.AnchorUnderMouse,
)

ViewportAnchorStr = Literal["none", "view_center", "under_mouse"]

VIEWPORT_UPDATE_MODE = bidict(
    full=QtWidgets.QGraphicsView.FullViewportUpdate,
    minimal=QtWidgets.QGraphicsView.MinimalViewportUpdate,
    smart=QtWidgets.QGraphicsView.SmartViewportUpdate,
    bounding_rect=QtWidgets.QGraphicsView.BoundingRectViewportUpdate,
    none=QtWidgets.QGraphicsView.NoViewportUpdate,
)

ViewportUpdateModeStr = Literal["full", "minimal", "smart", "bounding_rect", "none"]


QtWidgets.QGraphicsView.__bases__ = (widgets.AbstractScrollArea,)


class GraphicsView(QtWidgets.QGraphicsView):
    def serialize_fields(self):
        return dict(
            scene=self.scene(),
            background_brush=gui.Brush(self.backgroundBrush()),
            foreground_brush=gui.Brush(self.foregroundBrush()),
            transformation_anchor=self.get_transformation_anchor(),
            resize_anchor=self.get_resize_anchor(),
            viewport_update_mode=self.get_viewport_update_mode(),
            drag_mode=self.get_drag_mode(),
            rubberband_selection_mode=self.get_rubberband_selection_mode(),
            scene_rect=core.RectF(self.sceneRect()),
            cache_mode=self.get_cache_mode(),
            is_interactive=self.isInteractive(),
        )

    def __getitem__(self, index: int) -> QtWidgets.QGraphicsItem:
        return self.items()[index]

    def invalidate_scene(
        self, rect: QtCore.QRectF, layer: widgets.graphicsscene.SceneLayerStr = "all"
    ):
        if layer not in widgets.graphicsscene.SCENE_LAYER:
            raise InvalidParamError(layer, widgets.graphicsscene.SCENE_LAYER)
        self.invalidateScene(rect, widgets.graphicsscene.SCENE_LAYER[layer])

    def set_transformation_anchor(self, mode: ViewportAnchorStr):
        """Set how the view should position the scene during transformations.

        Args:
            mode: transformation anchor to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_ANCHOR:
            raise InvalidParamError(mode, VIEWPORT_ANCHOR)
        self.setTransformationAnchor(VIEWPORT_ANCHOR[mode])

    def get_transformation_anchor(self) -> ViewportAnchorStr:
        """Return current transformation anchor.

        Returns:
            viewport anchor
        """
        return VIEWPORT_ANCHOR.inverse[self.transformationAnchor()]

    def set_resize_anchor(self, mode: ViewportAnchorStr):
        """Set how the view should position the scene during resizes.

        Args:
            mode: resize anchor to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_ANCHOR:
            raise InvalidParamError(mode, VIEWPORT_ANCHOR)
        self.setResizeAnchor(VIEWPORT_ANCHOR[mode])

    def get_resize_anchor(self) -> ViewportAnchorStr:
        """Return current resize anchor.

        Returns:
            resize anchor
        """
        return VIEWPORT_ANCHOR.inverse[self.resizeAnchor()]

    def set_viewport_update_mode(self, mode: ViewportUpdateModeStr):
        """Set how the viewport should update its contents.

        Args:
            mode: viewport update mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_UPDATE_MODE:
            raise InvalidParamError(mode, VIEWPORT_UPDATE_MODE)
        self.setViewportUpdateMode(VIEWPORT_UPDATE_MODE[mode])

    def get_viewport_update_mode(self) -> ViewportUpdateModeStr:
        """Return current viewport update mode.

        Returns:
            viewport update mode
        """
        return VIEWPORT_UPDATE_MODE.inverse[self.viewportUpdateMode()]

    def set_drag_mode(self, mode: DragModeStr):
        """Set the behavior for dragging the mouse while the left mouse button is pressed.

        Args:
            mode: drag mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in DRAG_MODE:
            raise InvalidParamError(mode, DRAG_MODE)
        self.setDragMode(DRAG_MODE[mode])

    def get_drag_mode(self) -> DragModeStr:
        """Return current drag mode.

        Returns:
            drag mode
        """
        return DRAG_MODE.inverse[self.dragMode()]

    def set_rubberband_selection_mode(self, mode: constants.ItemSelectionModeStr):
        """Set the behavior for selecting items with a rubber band selection rectangle.

        Args:
            mode: rubberband selection mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in constants.ITEM_SELECTION_MODE:
            raise InvalidParamError(mode, constants.ITEM_SELECTION_MODE)
        self.setRubberBandSelectionMode(constants.ITEM_SELECTION_MODE[mode])

    def get_rubberband_selection_mode(self) -> constants.ItemSelectionModeStr:
        """Return current rubberband selection mode.

        Returns:
            rubberband selection mode
        """
        return constants.ITEM_SELECTION_MODE.inverse[self.rubberBandSelectionMode()]

    def set_cache_mode(self, mode: CacheModeStr):
        """Set the cache mode.

        Args:
            mode: cache mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in CACHE_MODES:
            raise InvalidParamError(mode, CACHE_MODES)
        self.setCacheMode(CACHE_MODES[mode])

    def get_cache_mode(self) -> CacheModeStr:
        """Return current cache mode.

        Returns:
            cache mode
        """
        return CACHE_MODES.inverse[self.cacheMode()]

    def set_optimization_flags(self, *items: str):
        for item in items:
            if item not in OPTIMIZATION_FLAGS:
                raise InvalidParamError(item, OPTIMIZATION_FLAGS)
        flags = helpers.merge_flags(items, OPTIMIZATION_FLAGS)
        self.setOptimizationFlags(flags)

    def get_optimization_flags(self) -> List[str]:
        return [k for k, v in OPTIMIZATION_FLAGS.items() if v & self.optimizationFlags()]


if __name__ == "__main__":
    app = widgets.app()
    view = GraphicsView()
    scene = widgets.GraphicsScene()
    scene.add_line(core.Line(0, 0, 200, 100))
    view.setScene(scene)
    view.show()
    app.main_loop()
