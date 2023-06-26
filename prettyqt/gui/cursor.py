from __future__ import annotations

import logging
from typing import Literal

from prettyqt import constants, core, gui
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import serializemixin

logger = logging.getLogger(__name__)


class Cursor(serializemixin.SerializeMixin, QtGui.QCursor):
    @classmethod
    def fake_mouse_move(cls):
        cls.setPos(cls.pos() + core.Point(0, 1))
        gui.Application.processEvents()
        cls.setPos(cls.pos() - core.Point(0, 1))

    @classmethod
    def click(cls, key=QtCore.Qt.MouseButton.LeftButton):
        from prettyqt import widgets

        app = widgets.app()
        widget = app.widgetAt(cls.pos())
        if widget is None:
            return
        pos = cls.pos().toPointF()
        local = pos - widget.mapToGlobal(core.PointF(0, 0))
        logger.info(f"sending MouseClick events to {widget} at {local}")
        event = gui.QMouseEvent(
            QtCore.QEvent.Type.MouseButtonPress,
            local,
            pos,
            key,
            QtCore.Qt.MouseButton.NoButton,
            QtCore.Qt.KeyboardModifier(0),
        )

        core.CoreApplication.sendEvent(widget, event)
        event = gui.QMouseEvent(
            QtCore.QEvent.Type.MouseButtonRelease,
            local,
            pos,
            key,
            QtCore.Qt.MouseButton.NoButton,
            QtCore.Qt.KeyboardModifier(0),
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
        where: Literal["screen", "current"] | QtGui.QScreen
        # | QtWidgets.QWidget
        | QtCore.QRect | QtCore.QPoint | tuple[int, int] | tuple[int, int, int, int],
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
            case QtCore.QPoint():
                geom = core.Rect(where, where)
            case (int(), int()):
                p = core.Point(*where)
                geom = core.Rect(p, p)
            case (int(), int(), int(), int()):
                geom = core.Rect(*where)
            case QtCore.QRect():
                geom = where
            case "screen":
                geom = gui.GuiApplication.primaryScreen().geometry()
            case QtGui.QScreen():
                geom = where.geometry()
            case _:  # not wanting to import QtWidgets here... perhaps create a protocol.
                geom = where.frameGeometry()
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
        new_pos = core.Point(new.x() + x_offset, new.y() + y_offset)
        if duration > 0:
            from prettyqt.custom_animations import cursormoveanimation

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
