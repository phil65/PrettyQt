from __future__ import annotations

from prettyqt import constants, core, gui, widgets


PAINTING_SCALE_FACTOR = 20.0
DIAMOND_POLYGON = gui.PolygonF.create_diamond()
STAR_POLYGON = gui.PolygonF.create_star()


class StarRating:
    """Handle the actual painting of the stars themselves."""

    def __init__(self, star_count: int = 1, max_stars: int = 5):
        self.star_count = star_count
        self.max_stars = max_stars

    def sizeHint(self):
        return PAINTING_SCALE_FACTOR * core.Size(self.max_stars, 1)  # type: ignore

    def paint(
        self,
        painter: gui.QPainter,
        rect: core.QRect,
        palette: gui.QPalette,
        is_editable: bool = False,
    ):
        """Paint the stars (and/or diamonds if we're in editing mode)."""
        painter.save()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setPen(constants.PenStyle.NoPen)
        painter.setBrush(palette.highlight() if is_editable else palette.windowText())
        y_offset = (rect.height() - PAINTING_SCALE_FACTOR) / 2
        painter.translate(rect.x() + 10, rect.y() + 10 + y_offset)
        painter.scale(PAINTING_SCALE_FACTOR, PAINTING_SCALE_FACTOR)
        for i in range(self.max_stars):
            if i < self.star_count:
                painter.drawPolygon(STAR_POLYGON, constants.FillRule.WindingFill)
            elif is_editable:
                painter.drawPolygon(DIAMOND_POLYGON, constants.FillRule.WindingFill)
            else:
                break
            painter.translate(1.0, 0.0)
        painter.restore()


class StarEditor(widgets.Widget):
    """The custom editor for editing StarRatings."""

    # A signal to tell the delegate when we've finished editing.
    editing_finished = core.Signal()

    def __init__(self, parent: widgets.QWidget | None = None):
        """Initialize the editor object, making sure we can watch mouse events."""
        super().__init__(parent)

        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.star_rating = StarRating()

    def sizeHint(self) -> core.QSize:
        """Tell the caller how big we are."""
        return self.star_rating.sizeHint()

    def paintEvent(self, event):
        """Paint the editor, offloading the work to the StarRating class."""
        with gui.Painter(self) as painter:
            self.star_rating.paint(painter, self.rect(), self.palette(), is_editable=True)

    def mouseMoveEvent(self, event):
        """Update stars on mouse move."""
        star = self.star_at_position(event.position().x())

        if star != -1:
            self.star_rating.star_count = star
            self.update()

    def mouseReleaseEvent(self, event):
        """Once star rating was clicked, tell the delegate we're done editing."""
        self.editing_finished.emit()

    def star_at_position(self, x: float) -> int:
        """Calculate which star the user's mouse cursor is currently hovering over."""
        val = x // (self.star_rating.sizeHint().width() // self.star_rating.max_stars) + 1
        return val if 0 < val <= self.star_rating.max_stars else -1

    def set_star_rating(self, rating: int):
        self.star_rating.star_count = rating


class StarDelegate(widgets.StyledItemDelegate):
    """A delegate class that allows us to render our star ratings."""

    ID = "star"

    def paint(
        self,
        painter: gui.QPainter,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        star_rating = StarRating(index.data())

        # If the row is currently selected, we need to make sure we
        # paint the background accordingly.
        if option.state & widgets.Style.StateFlag.State_Selected:
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

    def sizeHint(self, option: widgets.QStyleOptionViewItem, index: core.ModelIndex):
        """Return the size needed to display the item in a QSize object."""
        star_rating = StarRating(index.data())
        return star_rating.sizeHint()

    # The next 4 methods handle the custom editing that we need to do.
    # If this were just a display delegate, paint() and sizeHint() would
    # be all we needed.

    def createEditor(
        self,
        parent: widgets.QWidget,
        option: widgets.QStyleOptionViewItem,
        index: core.ModelIndex,
    ):
        """Create and return the StarEditor object we'll use to edit the StarRating."""
        editor = StarEditor(parent)
        editor.editing_finished.connect(self.commitAndCloseEditor)
        return editor

    def setEditorData(self, editor: StarEditor, index: core.ModelIndex):
        """Set the data to be displayed and edited by our custom editor."""
        editor.set_star_rating(index.data())

    def setModelData(
        self,
        editor: widgets.QWidget,
        model: core.QAbstractItemModel,
        index: core.ModelIndex,
    ):
        """Get the data from our custom editor and stuffs it into the model."""
        model.setData(index, editor.star_rating.star_count)

    def commitAndCloseEditor(self):
        editor = self.sender()

        # The commitData signal must be emitted when we've finished editing
        # and need to write our changed back to the model.
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, self.EndEditHint.NoHint)


if __name__ == "__main__":
    app = widgets.app()
    table_widget = widgets.TableWidget(1, 2)
    table_widget.set_delegate(StarDelegate(), column=1)
    table_widget.set_edit_triggers("all")
    table_widget.set_selection_behavior("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Rating"])

    item_1 = widgets.TableWidgetItem("Test1")
    item_2 = widgets.TableWidgetItem()
    item_2.setData(constants.DISPLAY_ROLE, 3)
    table_widget[0, 0] = item_1
    table_widget[0, 1] = item_2

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.exec()
