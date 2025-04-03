from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core, gui
from prettyqt.utils import serializemixin


if TYPE_CHECKING:
    from prettyqt import widgets


logger = logging.getLogger(__name__)


class Cursor(serializemixin.SerializeMixin, gui.QCursor):
    """Provides a mouse cursor with an arbitrary shape.

    This class is mainly used to create mouse cursors that are associated
    with particular widgets and to get and set the position of the mouse cursor.
    Qt has a number of standard cursor shapes, but you can also make custom cursor
    shapes based on a QBitmap, a mask and a hotspot.
    To associate a cursor with a widget, use `widget.set_cursor()`.
    To associate a cursor with all widgets (normally for a short period of time),
    use `GuiApplication.set_override_cursor()`.
    To set a cursor shape use `QCursor.setShape()` or use the QCursor
    constructor which takes the shape as argument, or you can use one of the
    predefined cursors defined in the `Qt.CursorShape` enum.
    If you want to create a cursor with your own bitmap,
    either use the QCursor constructor which takes a bitmap and a mask
    or the constructor which takes a pixmap as arguments.
    To set or get the position of the mouse cursor use the
    static methods `QCursor.pos()` and `QCursor.setPos()`.

    !!! note:
        It is possible to create a QCursor before QGuiApplication,
        but it is not useful except as a place-holder for a real QCursor
        created after QGuiApplication.
        Attempting to use a QCursor that was created before QGuiApplication will
        result in a crash.

    """

    @classmethod
    def fake_mouse_move(cls):
        cls.setPos(cls.pos() + core.Point(0, 1))
        gui.GuiApplication.processEvents()
        cls.setPos(cls.pos() - core.Point(0, 1))

    @classmethod
    def click(cls, key=constants.MouseButton.LeftButton):
        from prettyqt import widgets

        app = widgets.app()
        widget = app.widgetAt(cls.pos())
        if widget is None:
            return
        pos = cls.pos().toPointF()
        local = pos - widget.mapToGlobal(core.PointF(0, 0))
        logger.info("sending MouseClick events to %s at %s", widget, local)
        event = gui.QMouseEvent(
            core.QEvent.Type.MouseButtonPress,
            local,
            pos,
            key,
            constants.MouseButton.NoButton,
            constants.KeyboardModifier(0),
        )

        core.CoreApplication.sendEvent(widget, event)
        event = gui.QMouseEvent(
            core.QEvent.Type.MouseButtonRelease,
            local,
            pos,
            key,
            constants.MouseButton.NoButton,
            constants.KeyboardModifier(0),
        )

        core.CoreApplication.sendEvent(widget, event)

    def set_shape(self, shape: constants.CursorShapeStr):
        """Set cursor shape.

        Args:
            shape: shape to use
        """
        self.setShape(constants.CURSOR_SHAPE.get_enum_value(shape))

    def get_shape(self) -> constants.CursorShapeStr:
        """Return current cursor shape.

        Returns:
            cursor shape
        """
        return constants.CURSOR_SHAPE.inverse[self.shape()]

    @classmethod
    def get_pos(cls) -> core.Point:
        return core.Point(cls.pos())

    @classmethod
    def set_pos(
        cls,
        where: (
            Literal["screen", "current"]
            | gui.QScreen
            | widgets.QWidget
            | core.QRect
            | core.QPoint
            | tuple[int, int]
            | tuple[int, int, int, int]
        ),
        how: Literal[
            "center",
            "top",
            "left",
            "bottom",
            "right",
            "top_left",
            "top_right",
            "bottom_left",
            "bottom_right",
        ] = "center",
        x_offset: int = 0,
        y_offset: int = 0,
        duration: int = 0,
    ):
        """Position cursor onto screen position / widget / window / screen.

        Arguments:
            where: where to position on
            how: How to align
            x_offset: additional x offset for final position
            y_offset: additional y offset for final position
            duration: movement time
        """
        match where:
            case "current":
                p = cls.pos()
                geom = core.Rect(p, p)
            case core.QPoint():
                geom = core.Rect(where, where)
            case (int(), int()):
                p = core.Point(*where)
                geom = core.Rect(p, p)
            case (int(), int(), int(), int()):
                geom = core.Rect(*where)
            case core.QRect():
                geom = where
            case "screen":
                geom = gui.GuiApplication.primaryScreen().geometry()
            case gui.QScreen():
                geom = where.geometry()
            case _ if hasattr(where, "frameGeometry"):  # avoiding to import widgets here
                geom = where.frameGeometry()
            case _:
                raise TypeError(where)
        match how:
            case "center":
                new = geom.center()
            case "top":
                new = core.Point(geom.center().x(), geom.top())
            case "bottom":
                new = core.Point(geom.center().x(), geom.bottom())
            case "left":
                new = core.Point(geom.left(), geom.center().y())
            case "right":
                new = core.Point(geom.right(), geom.center().y())
            case "top_right":
                new = geom.topRight()
            case "top_left":
                new = geom.topLeft()
            case "bottom_right":
                new = geom.bottomRight()
            case "bottom_left":
                new = geom.bottomLeft()
            case _:
                raise TypeError(how)
        new_pos = core.Point(new.x() + x_offset, new.y() + y_offset)
        if duration > 0:
            from prettyqt.animations import cursormoveanimation

            cls._cursor_animation = cursormoveanimation.CursorMoveAnimation(
                duration=duration, end=new_pos
            )
            cls._cursor_animation.start()
        else:
            cls.setPos(new_pos)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.PushButton()
    widget.show()
    with app.debug_mode():
        app.sleep(2)
        widget.clicked.connect(lambda: logger.info("x"))
        Cursor.set_pos("screen", duration=1000)
        app.sleep(2)
        Cursor.set_pos(widget, how="right")
