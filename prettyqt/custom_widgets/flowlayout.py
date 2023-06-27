from __future__ import annotations

from prettyqt import constants, core, gui, widgets


class FlowLayout(widgets.Layout):
    ID = "flow"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._items = []

    def __add__(self, other: widgets.QWidget | widgets.QLayout) -> FlowLayout:
        if not isinstance(other, widgets.QWidget | widgets.QLayout):
            raise TypeError()
        self.add(other)
        return self

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addLayout(self, layout: widgets.QLayout):
        widget = widgets.Widget()
        widget.setLayout(layout)
        self.addWidget(widget)

    def addItem(self, item):
        self._items.append(item)

    def itemAt(self, idx):
        try:
            return self._items[idx]
        except IndexError:
            pass

    def takeAt(self, idx):
        try:
            return self._items.pop(idx)
        except IndexError:
            pass

    def count(self):
        return len(self._items)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(core.Rect(0, 0, width, 0), apply_geometry=False)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, apply_geometry=True)

    def expandingDirections(self):
        return constants.Orientation(0)

    def minimumSize(self):
        size = core.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        return size + core.QSize(left + right, top + bottom)

    sizeHint = minimumSize

    def smart_spacing(self, horizontal: bool = True) -> int:
        p = self.parent()
        if p is None:
            return -1
        if p.isWidgetType():
            which = (
                widgets.Style.PixelMetric.PM_LayoutHorizontalSpacing
                if horizontal
                else widgets.Style.PixelMetric.PM_LayoutVerticalSpacing
            )
            return p.style().pixelMetric(which, None, p)
        return p.spacing()

    def _do_layout(self, rect: core.QRect, apply_geometry: bool = False) -> int:
        erect = rect.marginsRemoved(self.contentsMargins())
        x, y = erect.x(), erect.y()

        line_height = 0

        def layout_spacing(wid, horizontal: bool = True):
            if (ans := self.smart_spacing(horizontal)) != -1:
                return ans
            if wid is None:
                return 0
            return wid.style().layoutSpacing(
                widgets.SizePolicy.ControlType.PushButton,
                widgets.SizePolicy.ControlType.PushButton,
                constants.HORIZONTAL if horizontal else constants.VERTICAL,
            )

        lines, current_line = [], []
        gmap = {}
        for item in self._items:
            isz, wid = item.sizeHint(), item.widget()
            hs, vs = layout_spacing(wid), layout_spacing(wid, False)

            next_x = x + isz.width() + hs
            if next_x - hs > erect.right() and line_height > 0:
                x = erect.x()
                y = y + line_height + vs
                next_x = x + isz.width() + hs
                lines.append((line_height, current_line))
                current_line = []
                line_height = 0
            if apply_geometry:
                gmap[item] = x, y, isz
            x = next_x
            line_height = max(line_height, isz.height())
            current_line.append((item, isz.height()))

        lines.append((line_height, current_line))

        if apply_geometry:
            for line_height, items in lines:
                for item, item_height in items:
                    x, wy, isz = gmap[item]
                    if item_height < line_height:
                        wy += (line_height - item_height) // 2
                    item.setGeometry(core.Rect(core.Point(x, wy), isz))

        return y + line_height - rect.y() + self.contentsMargins().bottom()


class Separator(widgets.Widget):
    """Vertical separator lines usable in FlowLayout."""

    def __init__(
        self, *args, widget_for_height: widgets.QWidget | None = None, **kwargs
    ):
        """You must provide a widget in the layout either here or with setBuddy.

        The height of the separator is computed using this widget,
        """
        super().__init__(*args, **kwargs)
        self.bcol = widgets.app().palette().color(gui.Palette.ColorRole.Text)
        self.update_brush()
        self.widget_for_height = widget_for_height
        self.set_size_policy("fixed", "minimum_expanding")

    def update_brush(self):
        self.brush = gui.Brush(self.bcol)
        self.update()

    def setBuddy(self, widget_for_height: widgets.QWidget):
        """See __init__. This is repurposed to support Qt Designer .ui files."""
        self.widget_for_height = widget_for_height

    def sizeHint(self):
        return core.QSize(
            1, 1 if self.widget_for_height is None else self.widget_for_height.height()
        )

    def paintEvent(self, ev):
        with gui.Painter(self) as painter:
            # Purely subjective: shorten the line a bit to look 'better'
            r = ev.rect()
            r.setTop(r.top() + 3)
            r.setBottom(r.bottom() - 3)
            painter.fillRect(r, self.brush)


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.Widget()
    layout = FlowLayout()
    layout.add(widgets.PushButton("Short"))
    layout.add(widgets.PushButton("Longer"))
    layout.add(widgets.PushButton("Different text"))
    layout.add(widgets.PushButton("More text"))
    layout.add(widgets.PushButton("Even longer button text"))
    widget.set_layout(layout)
    widget.show()
    app.exec()
