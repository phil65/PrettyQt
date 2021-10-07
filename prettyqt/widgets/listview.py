from __future__ import annotations

from typing import Literal

from prettyqt import core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


VIEW_MODE = bidict(
    list=QtWidgets.QListView.ViewMode.ListMode, icon=QtWidgets.QListView.ViewMode.IconMode
)

ViewModeStr = Literal["list", "icon"]

MOVEMENT = bidict(
    static=QtWidgets.QListView.Movement.Static,
    free=QtWidgets.QListView.Movement.Free,
    snap=QtWidgets.QListView.Movement.Snap,
)

MovementStr = Literal["static", "free", "snap"]

FLOW = bidict(
    left_to_right=QtWidgets.QListView.Flow.LeftToRight,
    top_to_bottom=QtWidgets.QListView.Flow.TopToBottom,
)

FlowStr = Literal["left_to_right", "top_to_bottom"]

LAYOUT_MODE = bidict(
    single_pass=QtWidgets.QListView.LayoutMode.SinglePass,
    batched=QtWidgets.QListView.LayoutMode.Batched,
)

LayoutModeStr = Literal["single_pass", "batched"]

RESIZE_MODE = bidict(
    fixed=QtWidgets.QListView.ResizeMode.Fixed,
    adjust=QtWidgets.QListView.ResizeMode.Adjust,
)

ResizeModeStr = Literal["fixed", "adjust"]


QtWidgets.QListView.__bases__ = (widgets.AbstractItemView,)


class ListView(QtWidgets.QListView):
    def serialize_fields(self):
        return dict(
            view_mode=self.get_view_mode(),
            resize_mode=self.get_resize_mode(),
            layout_mode=self.get_layout_mode(),
            movement=self.get_movement(),
            batch_size=self.batchSize(),
            flow=self.get_flow(),
            grid_size=self.get_grid_size(),
            is_wrapping=self.isWrapping(),
            # item_alignment=self.itemAlignment(),
            model_column=self.modelColumn(),
            selection_rect_visible=self.isSelectionRectVisible(),
            spacing=self.spacing(),
            uniform_item_sizes=self.uniformItemSizes(),
            word_wrap=self.wordWrap(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_view_mode(state["view_mode"])
        self.set_resize_mode(state["resize_mode"])
        self.set_layout_mode(state["layout_mode"])
        self.set_movement(state["movement"])
        self.setBatchSize(state["batch_size"])
        self.set_flow(state["flow"])
        self.set_grid_size(state["grid_size"])
        self.setWrapping(state["is_wrapping"])
        # self.setItemAlignment(state["flow"])
        self.setModelColumn(state["model_column"])
        self.setSelectionRectVisible(state["selection_rect_visible"])
        self.setSpacing(state["spacing"])
        self.setUniformItemSizes(state["uniform_item_sizes"])
        self.setWordWrap(state["word_wrap"])

    def set_view_mode(self, mode: ViewModeStr):
        """Set view mode.

        Args:
            mode: view mode to use

        Raises:
            InvalidParamError: invalid view mode
        """
        if mode not in VIEW_MODE:
            raise InvalidParamError(mode, VIEW_MODE)
        self.setViewMode(VIEW_MODE[mode])

    def get_view_mode(self) -> ViewModeStr:
        """Return view mode.

        Returns:
            view mode
        """
        return VIEW_MODE.inverse[self.viewMode()]

    def set_resize_mode(self, mode: ResizeModeStr):
        """Set resize mode.

        Args:
            mode: resize mode to use

        Raises:
            InvalidParamError: invalid resize mode
        """
        if mode not in RESIZE_MODE:
            raise InvalidParamError(mode, RESIZE_MODE)
        self.setResizeMode(RESIZE_MODE[mode])

    def get_resize_mode(self) -> ResizeModeStr:
        """Return resize mode.

        Returns:
            resize mode
        """
        return RESIZE_MODE.inverse[self.resizeMode()]

    def set_layout_mode(self, mode: LayoutModeStr):
        """Set layout mode.

        Args:
            mode: layout mode to use

        Raises:
            InvalidParamError: invalid layout mode
        """
        if mode not in LAYOUT_MODE:
            raise InvalidParamError(mode, LAYOUT_MODE)
        self.setLayoutMode(LAYOUT_MODE[mode])

    def get_layout_mode(self) -> LayoutModeStr:
        """Return layout mode.

        Returns:
            layout mode
        """
        return LAYOUT_MODE.inverse[self.layoutMode()]

    def set_movement(self, mode: MovementStr):
        """Set movement mode.

        Args:
            mode: movement mode to use

        Raises:
            InvalidParamError: invalid movement mode
        """
        if mode not in MOVEMENT:
            raise InvalidParamError(mode, MOVEMENT)
        self.setMovement(MOVEMENT[mode])

    def get_movement(self) -> MovementStr:
        """Return movement mode.

        Returns:
            movement mode
        """
        return MOVEMENT.inverse[self.movement()]

    def set_flow(self, mode: FlowStr):
        """Set flow mode.

        Args:
            mode: flow mode to use

        Raises:
            InvalidParamError: invalid flow mode
        """
        if mode not in FLOW:
            raise InvalidParamError(mode, FLOW)
        self.setFlow(FLOW[mode])

    def get_flow(self) -> FlowStr:
        """Return flow mode.

        Returns:
            flow mode
        """
        return FLOW.inverse[self.flow()]

    def set_grid_size(self, size: QtCore.QSize | tuple[int, int]):
        if isinstance(size, tuple):
            size = QtCore.QSize(*size)
        self.setGridSize(size)

    def get_grid_size(self) -> core.Size:
        return core.Size(self.gridSize())


if __name__ == "__main__":
    app = widgets.app()
    dlg = ListView()
    dlg.show()
    app.main_loop()
