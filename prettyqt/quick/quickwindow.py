from __future__ import annotations

import contextlib
from typing import Literal

from prettyqt import gui
from prettyqt.qt import QtCore, QtGui, QtQuick
from prettyqt.utils import InvalidParamError, bidict


CREATE_TEXTURE_OPTION = bidict(
    has_alpha_channel=QtQuick.QQuickWindow.CreateTextureOption.TextureHasAlphaChannel,
    has_mipmaps=QtQuick.QQuickWindow.CreateTextureOption.TextureHasMipmaps,
    owns_gl_texture=QtQuick.QQuickWindow.CreateTextureOption.TextureOwnsGLTexture,
    can_use_atlas=QtQuick.QQuickWindow.CreateTextureOption.TextureCanUseAtlas,
    is_opaque=QtQuick.QQuickWindow.CreateTextureOption.TextureIsOpaque,
)

CreateTextureOptionStr = Literal[
    "has_alpha_channel",
    "has_mipmaps",
    "owns_gl_texture",
    "can_use_atlas",
    "is_opaque",
]

RENDER_STAGE = bidict(
    before_synchronizing=QtQuick.QQuickWindow.RenderStage.BeforeSynchronizingStage,
    after_synchronizing=QtQuick.QQuickWindow.RenderStage.AfterSynchronizingStage,
    before_rendering=QtQuick.QQuickWindow.RenderStage.BeforeRenderingStage,
    after_rendering=QtQuick.QQuickWindow.RenderStage.AfterRenderingStage,
    after_swap=QtQuick.QQuickWindow.RenderStage.AfterSwapStage,
    no_stage=QtQuick.QQuickWindow.RenderStage.NoStage,
)

RenderStageStr = Literal[
    "before_synchronizing",
    "after_synchronizing",
    "before_rendering",
    "after_rendering",
    "after_swap",
    "no_stage",
]

TEXT_RENDER_TYPE = bidict(
    qt_text=QtQuick.QQuickWindow.TextRenderType.QtTextRendering,
    native_text=QtQuick.QQuickWindow.TextRenderType.NativeTextRendering,
)

TextRenderTypeStr = Literal["qt_text", "native_text"]


QtQuick.QQuickWindow.__bases__ = (gui.Window,)


class QuickWindow(QtQuick.QQuickWindow):
    def create_texture_from_image(self, image: QtGui.QImage, **kwargs):
        flag = self.CreateTextureOption(0)
        for key, val in kwargs.items():
            if val is True:
                v = CREATE_TEXTURE_OPTION[key]
                flag |= v
        return self.createTextureFromImage(image, flag)  # type: ignore

    def grab_window(self) -> gui.Image:
        return gui.Image(self.grabWindow())

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    @staticmethod
    def set_text_render_type(typ: TextRenderTypeStr):
        """Set the default render type of text-like elements in Qt Quick.

        Note: setting the render type will only affect elements created afterwards;
        the render type of existing elements will not be modified.

        Args:
            typ: text render type to use

        Raises:
            InvalidParamError: text render type does not exist
        """
        if typ not in TEXT_RENDER_TYPE:
            raise InvalidParamError(typ, TEXT_RENDER_TYPE)
        QuickWindow.setTextRenderType(TEXT_RENDER_TYPE[typ])

    @staticmethod
    def get_text_render_type() -> TextRenderTypeStr:
        """Return the render type of text-like elements in Qt Quick.

        Returns:
            text render type
        """
        return TEXT_RENDER_TYPE.inverse[QuickWindow.textRenderType()]

    @contextlib.contextmanager
    def external_commands(self):
        self.beginExternalCommands()
        yield self
        self.endExternalCommands()

    def schedule_render_job(self, job: QtCore.QRunnable, render_stage: RenderStageStr):
        if render_stage not in RENDER_STAGE:
            raise InvalidParamError(render_stage, RENDER_STAGE)
        self.scheduleRenderJob(job, RENDER_STAGE[render_stage])


if __name__ == "__main__":
    app = gui.GuiApplication([])
    wnd = QuickWindow()
    img = QtGui.QImage()
    texture = wnd.create_texture_from_image(img)
