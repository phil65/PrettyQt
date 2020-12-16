import math
from typing import Optional

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets


PAINTING_SCALE_FACTOR = 20
DIAMOND_POINTS = [
    core.PointF(0.4, 0.5),
    core.PointF(0.5, 0.4),
    core.PointF(0.6, 0.5),
    core.PointF(0.5, 0.6),
    core.PointF(0.4, 0.5),
]


class StarRating:
    """Handle the actual painting of the stars themselves."""

    def __init__(self, star_count=1, max_stars=5):
        self.star_count = star_count
        self.max_stars = max_stars

        # Create the star shape we'll be drawing.
        self.star_polygon = gui.PolygonF()
        self.star_polygon += core.PointF(1.0, 0.5)
        for i in range(1, 5):
            val = 0.8 * i * math.pi
            point = core.PointF(0.5 + 0.5 * math.cos(val), 0.5 + 0.5 * math.sin(val))
            self.star_polygon += point

        # Create the diamond shape we'll show in the editor
        self.diamond_polygon = gui.PolygonF()
        self.diamond_polygon.add_points(*DIAMOND_POINTS)

    def sizeHint(self):
        """Tell the caller how big we are."""
        return PAINTING_SCALE_FACTOR * core.Size(self.max_stars, 1)

    def paint(
        self,
        painter: QtGui.QPainter,
        rect: QtCore.QRect,
        palette: QtGui.QPalette,
        is_editable: bool = False,
    ):
        """Paint the stars (and/or diamonds if we're in editing mode)."""
        painter.save()
        painter.setRenderHint(painter.Antialiasing, True)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(palette.highlight() if is_editable else palette.windowText())
        y_offset = (rect.height() - PAINTING_SCALE_FACTOR) / 2
        painter.translate(rect.x(), rect.y() + y_offset)
        painter.scale(PAINTING_SCALE_FACTOR, PAINTING_SCALE_FACTOR)
        for i in range(self.max_stars):
            if i < self.star_count:
                painter.drawPolygon(self.star_polygon, QtCore.Qt.WindingFill)
            elif is_editable:
                painter.drawPolygon(self.diamond_polygon, QtCore.Qt.WindingFill)
            painter.translate(1.0, 0.0)
        painter.restore()


class StarEditor(widgets.Widget):
    """The custom editor for editing StarRatings."""

    # A signal to tell the delegate when we've finished editing.
    editing_finished = core.Signal()

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        """Initialize the editor object, making sure we can watch mouse events."""
        super().__init__(parent)

        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.star_rating = StarRating()

    def sizeHint(self):
        """Tell the caller how big we are."""
        return self.star_rating.sizeHint()

    def paintEvent(self, event):
        """Paint the editor, offloading the work to the StarRating class."""
        painter = gui.Painter(self)
        self.star_rating.paint(painter, self.rect(), self.palette(), is_editable=True)

    def mouseMoveEvent(self, event):
        """Update stars on mouse move."""
        star = self.star_at_position(event.x())

        if star != -1:
            self.star_rating.star_count = star
            self.update()

    def mouseReleaseEvent(self, event):
        """Once star rating was clicked, tell the delegate we're done editing."""
        self.editing_finished.emit()

    def star_at_position(self, x: int) -> int:
        """Calculate which star the user's mouse cursor is currently hovering over."""
        val = x // (self.star_rating.sizeHint().width() // self.star_rating.max_stars) + 1
        if not 0 < val <= self.star_rating.max_stars:
            return -1
        return val

    def set_star_rating(self, rating: int):
        self.star_rating.star_count = rating


class StarDelegate(widgets.StyledItemDelegate):
    """A delegate class that allows us to render our star ratings."""

    def paint(self, painter, option, index):
        star_rating = StarRating(index.data())

        # If the row is currently selected, we need to make sure we
        # paint the background accordingly.
        if option.state & widgets.Style.State_Selected:
            # The original C++ example used option.palette.foreground() to
            # get the brush for painting, but there are a couple of
            # problems with that:
            #   - foreground() is obsolete now, use windowText() instead
            #   - more importantly, windowText() just returns a brush
            #     containing a flat color, where sometimes the style
            #     would have a nice subtle gradient or something.
            # Here we just use the brush of the painter object that's
            # passed in to us, which keeps the row highlighting nice
            # and consistent.
            painter.fillRect(option.rect, painter.brush())

        # Now that we've painted the background, call star_rating.paint()
        # to paint the stars.
        star_rating.paint(painter, option.rect, option.palette)

    def sizeHint(self, option, index):
        """Return the size needed to display the item in a QSize object."""
        star_rating = StarRating(index.data())
        return star_rating.sizeHint()

    # The next 4 methods handle the custom editing that we need to do.
    # If this were just a display delegate, paint() and sizeHint() would
    # be all we needed.

    def createEditor(self, parent, option, index):
        """Create and return the StarEditor object we'll use to edit the StarRating."""
        editor = StarEditor(parent)
        editor.editing_finished.connect(self.commitAndCloseEditor)
        return editor

    def setEditorData(self, editor, index):
        """Set the data to be displayed and edited by our custom editor."""
        editor.set_star_rating(index.data())

    def setModelData(self, editor, model, index):
        """Get the data from our custom editor and stuffs it into the model."""
        if index.column() == 3:
            model.setData(index, editor.star_rating.star_count)
        else:
            super().setModelData(self, editor, model, index)

    def commitAndCloseEditor(self):
        editor = self.sender()

        # The commitData signal must be emitted when we've finished editing
        # and need to write our changed back to the model.
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, self.NoHint)


if __name__ == "__main__":
    """Run the application."""
    from prettyqt import widgets

    app = widgets.app()

    # Create and populate the tableWidget
    table_widget = widgets.TableWidget(4, 4)
    table_widget.set_delegate(StarDelegate(), column=3)
    table_widget.setEditTriggers(
        widgets.AbstractItemView.DoubleClicked | widgets.AbstractItemView.SelectedClicked
    )
    table_widget.set_selection_behaviour("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Genre", "Artist", "Rating"])

    data = [
        ["Mass in B-Minor", "Baroque", "J.S. Bach", 5],
        ["Three More Foxes", "Jazz", "Maynard Ferguson", 4],
        ["Sex Bomb", "Pop", "Tom Jones", 3],
        ["Barbie Girl", "Pop", "Aqua", 5],
    ]

    for i, r in enumerate(data):
        table_widget[i, 0] = widgets.TableWidgetItem(r[0])
        table_widget[i, 1] = widgets.TableWidgetItem(r[1])
        table_widget[i, 2] = widgets.TableWidgetItem(r[2])
        item = widgets.TableWidgetItem()
        item.setData(0, StarRating(r[3]).star_count)
        table_widget[i, 3] = item

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.main_loop()
