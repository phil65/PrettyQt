from typing import Literal

from qtpy import QtGui

from prettyqt import gui
from prettyqt.utils import bidict


UPDATE_BEHAVIOUR = bidict(
    no_partial=QtGui.QOpenGLWindow.NoPartialUpdate,
    partial_blit=QtGui.QOpenGLWindow.PartialUpdateBlit,
    partial_blend=QtGui.QOpenGLWindow.PartialUpdateBlend,
)

UpdateBehaviourStr = Literal["no_partial", "partial_blit", "partial_blend"]


QtGui.QOpenGLWindow.__bases__ = (gui.PaintDeviceWindow,)


class OpenGLWindow(QtGui.QOpenGLWindow):
    def __bool__(self):
        return self.isValid()

    def get_update_behaviour(self) -> UpdateBehaviourStr:
        """Get the window update hehaviour.

        Returns:
            update behaviour
        """
        return UPDATE_BEHAVIOUR.inverse[self.updateBehavior()]

    def grab_framebuffer(self) -> gui.Image:
        return gui.Image(self.grabFramebuffer())


if __name__ == "__main__":
    app = gui.GuiApplication([])
    wnd = OpenGLWindow()
    print(bool(wnd))
    wnd.show()
    print(bool(wnd))
