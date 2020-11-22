import contextlib

from qtpy import QtQuick, QtGui, QtCore

from prettyqt import gui, core
from prettyqt.utils import bidict, InvalidParamError


CREATE_TEXTURE_OPTION = bidict(
    has_alpha_channel=QtQuick.QQuickWindow.TextureHasAlphaChannel,
    has_mipmaps=QtQuick.QQuickWindow.TextureHasMipmaps,
    owns_gl_texture=QtQuick.QQuickWindow.TextureOwnsGLTexture,
    can_use_atlas=QtQuick.QQuickWindow.TextureCanUseAtlas,
    is_opaque=QtQuick.QQuickWindow.TextureIsOpaque,
)

RENDER_STAGE = bidict(
    before_synchronizing=QtQuick.QQuickWindow.BeforeSynchronizingStage,
    after_synchronizing=QtQuick.QQuickWindow.AfterSynchronizingStage,
    before_rendering=QtQuick.QQuickWindow.BeforeRenderingStage,
    after_rendering=QtQuick.QQuickWindow.AfterRenderingStage,
    after_swap=QtQuick.QQuickWindow.AfterSwapStage,
    no_stage=QtQuick.QQuickWindow.NoStage,
)

TEXT_RENDER_TYPE = bidict(
    qt_text=QtQuick.QQuickWindow.QtTextRendering,
    native_text=QtQuick.QQuickWindow.NativeTextRendering,
)


QtQuick.QQuickWindow.__bases__ = (gui.Window,)


class QuickWindow(QtQuick.QQuickWindow):
    def create_texture_from_image(self, image: QtGui.QImage, **kwargs):
        flag = self.CreateTextureOption(0)
        for key, val in kwargs.items():
            if val is True:
                v = CREATE_TEXTURE_OPTION[key]
                flag |= v
        return self.createTextureFromImage(image, flag)

    def grab_window(self) -> gui.Image:
        return gui.Image(self.grabWindow())

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    def get_render_target_size(self) -> core.Size:
        return core.Size(self.renderTargetSize())

    @staticmethod
    def set_text_render_type(typ: str):
        """Set the default render type of text-like elements in Qt Quick.

        Note: setting the render type will only affect elements created afterwards;
        the render type of existing elements will not be modified.

        Allowed values are "qt_text", "native_text"

        Args:
            typ: text render type to use

        Raises:
            InvalidParamError: text render type does not exist
        """
        if typ not in TEXT_RENDER_TYPE:
            raise InvalidParamError(typ, TEXT_RENDER_TYPE)
        QuickWindow.setTextRenderType(TEXT_RENDER_TYPE[typ])

    @staticmethod
    def get_text_render_type() -> str:
        """Return the render type of text-like elements in Qt Quick.

        Possible values: "qt_text", "native_text"

        Returns:
            text render type
        """
        return TEXT_RENDER_TYPE.inv[QuickWindow.textRenderType()]

    @contextlib.contextmanager
    def external_commands(self):
        self.beginExternalCommands()
        yield self
        self.endExternalCommands()

    def schedule_render_job(self, job: QtCore.QRunnable, render_stage: str):
        if render_stage not in RENDER_STAGE:
            raise InvalidParamError(render_stage, RENDER_STAGE)
        self.scheduleRenderJob(job, RENDER_STAGE[render_stage])


if __name__ == "__main__":
    app = gui.GuiApplication([])
    wnd = QuickWindow()
    img = QtGui.QImage()
    texture = wnd.create_texture_from_image(img)
