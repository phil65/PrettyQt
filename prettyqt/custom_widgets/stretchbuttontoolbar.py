from __future__ import annotations

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore


class StretchButtonToolBar(widgets.ToolBar):
    """A QToolBar that dynamically resizes its tool buttons to fit available space.

    This is done by setting fixed size on the button instances.
    Note: the class does not support `QWidgetAction`, separators, etc.
    """

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        self._do_layout(size)

    def actionEvent(self, event):
        super().actionEvent(event)
        if event.type() in [core.Event.Type.ActionAdded, core.Event.Type.ActionRemoved]:
            self._do_layout(self.size())

    def sizeHint(self):
        hint = super().sizeHint()
        width, height = hint.width(), hint.height()
        m1 = self.contentsMargins()
        m2 = self.layout().contentsMargins()
        dx1, dy1, dw1, dh1 = m1.left(), m1.top(), m1.right(), m1.bottom()
        dx2, dy2, dw2, dh2 = m2.left(), m2.top(), m2.right(), m2.bottom()
        dx, dy = dx1 + dx2, dy1 + dy2
        dw, dh = dw1 + dw2, dh1 + dh2
        count = len(self.actions())
        spacing = self.layout().spacing()
        space_spacing = max(count - 1, 0) * spacing
        if self.orientation() == constants.HORIZONTAL:
            width = int(height * 1.618) * count + space_spacing + dw + dx
        else:
            height = int(width * 1.618) * count + space_spacing + dh + dy
        return QtCore.QSize(width, height)

    def _do_layout(self, size):
        """Layout the buttons to fit inside size."""
        geom = self.geometry()
        geom.setSize(size)

        # Adjust for margins (both the widgets and the layouts).
        geom = geom.marginsRemoved(self.contentsMargins())
        geom = geom.marginsRemoved(self.layout().contentsMargins())

        actions = self.actions()
        widgets_it = map(self.widgetForAction, actions)

        orientation = self.orientation()
        if orientation == constants.HORIZONTAL:
            widgets = sorted(widgets_it, key=lambda w: w.pos().x())
        else:
            widgets = sorted(widgets_it, key=lambda w: w.pos().y())

        spacing = self.layout().spacing()
        uniform_layout_helper(widgets, geom, orientation, spacing=spacing)


def uniform_layout_helper(items, contents_rect, expanding, spacing):
    """Set fixed sizes on 'items' so they can fill the whole space."""
    if len(items) == 0:
        return

    spacing_space = (len(items) - 1) * spacing

    if expanding == constants.HORIZONTAL:

        def setter(w, s):
            w.setFixedWidth(max(s, 0))

        space = contents_rect.width() - spacing_space
    else:

        def setter(w, s):
            w.setFixedHeight(max(s, 0))

        space = contents_rect.height() - spacing_space

    base_size = space // len(items)
    remainder = space % len(items)

    for i, item in enumerate(items):
        item_size = base_size + (1 if i < remainder else 0)
        setter(item, item_size)


if __name__ == "__main__":
    from prettyqt import gui

    app = widgets.app()
    widget = StretchButtonToolBar()
    actions = [
        gui.Action(
            text="super duper action",
            shortcut="Ctrl+A",
            tool_tip="some Tooltip text",
            icon="mdi.folder",
            triggered=lambda: print("test"),
        ),
        gui.Action(
            text="this is an action",
            shortcut="Ctrl+B",
            tool_tip="Tooltip",
            icon="mdi.folder-outline",
            checked=True,
            checkable=True,
        ),
    ]
    widget.addActions(actions)
    widget.show()
    app.exec()
