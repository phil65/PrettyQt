from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtOpenGLWidgets
from prettyqt.utils import bidict


TARGET_BUFFER = bidict(
    left_buffer=QtOpenGLWidgets.QOpenGLWidget.TargetBuffer.LeftBuffer,
    right_buffer=QtOpenGLWidgets.QOpenGLWidget.TargetBuffer.RightBuffer,
)

TargetBufferStr = Literal["left_buffer", "right_buffer"]


UPDATE_BEHAVIOR = bidict(
    no_partial=QtOpenGLWidgets.QOpenGLWidget.UpdateBehavior.NoPartialUpdate,
    partial=QtOpenGLWidgets.QOpenGLWidget.UpdateBehavior.PartialUpdate,
)

UpdateBehaviorStr = Literal["no_partial", "partial"]


class OpenGLWidget(widgets.WidgetMixin, QtOpenGLWidgets.QOpenGLWidget):
    """Widget for rendering OpenGL graphics."""

    def set_update_behavior(
        self, behavior: UpdateBehaviorStr | QtOpenGLWidgets.QOpenGLWidget.UpdateBehavior
    ):
        """Set update behavior.

        Args:
            behavior: update behavior to use
        """
        self.setUpdateBehavior(UPDATE_BEHAVIOR.get_enum_value(behavior))

    def get_update_behavior(self) -> UpdateBehaviorStr | None:
        """Return current update behavior.

        Returns:
            update behavior
        """
        return UPDATE_BEHAVIOR.inverse[self.updateBehavior()]

    def get_current_target_buffer(self) -> TargetBufferStr:
        """Return current target buffer.

        Returns:
            target buffer
        """
        return TARGET_BUFFER.inverse[self.currentTargetBuffer()]


if __name__ == "__main__":
    app = widgets.app()
    widget = OpenGLWidget()
    widget.show()
    app.exec()
