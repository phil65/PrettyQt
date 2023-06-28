from __future__ import annotations

from typing import Literal

from prettyqt import core, widgets
from prettyqt.utils import bidict, datatypes


ViewModeStr = Literal["list", "icon"]

VIEW_MODE: bidict[ViewModeStr, widgets.QListView.ViewMode] = bidict(
    list=widgets.QListView.ViewMode.ListMode, icon=widgets.QListView.ViewMode.IconMode
)

MovementStr = Literal["static", "free", "snap"]

MOVEMENT: bidict[MovementStr, widgets.QListView.Movement] = bidict(
    static=widgets.QListView.Movement.Static,
    free=widgets.QListView.Movement.Free,
    snap=widgets.QListView.Movement.Snap,
)

FlowStr = Literal["left_to_right", "top_to_bottom"]

FLOW: bidict[FlowStr, widgets.QListView.Flow] = bidict(
    left_to_right=widgets.QListView.Flow.LeftToRight,
    top_to_bottom=widgets.QListView.Flow.TopToBottom,
)

LayoutModeStr = Literal["single_pass", "batched"]

LAYOUT_MODE: bidict[LayoutModeStr, widgets.QListView.LayoutMode] = bidict(
    single_pass=widgets.QListView.LayoutMode.SinglePass,
    batched=widgets.QListView.LayoutMode.Batched,
)

ResizeModeStr = Literal["fixed", "adjust"]

RESIZE_MODE: bidict[ResizeModeStr, widgets.QListView.ResizeMode] = bidict(
    fixed=widgets.QListView.ResizeMode.Fixed,
    adjust=widgets.QListView.ResizeMode.Adjust,
)


class ListViewMixin(widgets.AbstractItemViewMixin):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "viewMode": VIEW_MODE,
            "resizeMode": RESIZE_MODE,
            "layoutMode": LAYOUT_MODE,
            "movement": MOVEMENT,
            "flow": FLOW,
        }
        return maps

    def set_view_mode(self, mode: ViewModeStr | widgets.QListView.ViewMode):
        """Set view mode.

        Args:
            mode: view mode to use
        """
        self.setViewMode(VIEW_MODE.get_enum_value(mode))

    def get_view_mode(self) -> ViewModeStr:
        """Return view mode.

        Returns:
            view mode
        """
        return VIEW_MODE.inverse[self.viewMode()]

    def set_resize_mode(self, mode: ResizeModeStr | widgets.QListView.ResizeMode):
        """Set resize mode.

        Args:
            mode: resize mode to use
        """
        self.setResizeMode(RESIZE_MODE.get_enum_value(mode))

    def get_resize_mode(self) -> ResizeModeStr:
        """Return resize mode.

        Returns:
            resize mode
        """
        return RESIZE_MODE.inverse[self.resizeMode()]

    def set_layout_mode(self, mode: LayoutModeStr | widgets.QListView.LayoutMode):
        """Set layout mode.

        Args:
            mode: layout mode to use
        """
        self.setLayoutMode(LAYOUT_MODE.get_enum_value(mode))

    def get_layout_mode(self) -> LayoutModeStr:
        """Return layout mode.

        Returns:
            layout mode
        """
        return LAYOUT_MODE.inverse[self.layoutMode()]

    def set_movement(self, mode: MovementStr | widgets.QListView.Movement):
        """Set movement mode.

        Args:
            mode: movement mode to use
        """
        self.setMovement(MOVEMENT.get_enum_value(mode))

    def get_movement(self) -> MovementStr:
        """Return movement mode.

        Returns:
            movement mode
        """
        return MOVEMENT.inverse[self.movement()]

    def set_flow(self, mode: FlowStr | widgets.QListView.Flow):
        """Set flow mode.

        Args:
            mode: flow mode to use
        """
        self.setFlow(FLOW.get_enum_value(mode))

    def get_flow(self) -> FlowStr:
        """Return flow mode.

        Returns:
            flow mode
        """
        return FLOW.inverse[self.flow()]

    def set_grid_size(self, size: datatypes.SizeType):
        self.setGridSize(datatypes.to_size(size))

    def get_grid_size(self) -> core.Size:
        return core.Size(self.gridSize())


class ListView(ListViewMixin, widgets.QListView):
    pass


if __name__ == "__main__":
    app = widgets.app()
    dlg = ListView()
    dlg.show()
    app.exec()
