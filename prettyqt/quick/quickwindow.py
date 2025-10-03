from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Literal

from prettyqt import gui
from prettyqt.qt import QtQuick
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from prettyqt.qt import QtCore


CreateTextureOptionStr = Literal[
    "has_alpha_channel",
    "has_mipmaps",
    "owns_gl_texture",
    "can_use_atlas",
    "is_opaque",
]

CREATE_TEXTURE_OPTION: bidict[
    CreateTextureOptionStr, QtQuick.QQuickWindow.CreateTextureOption
] = bidict(
    has_alpha_channel=QtQuick.QQuickWindow.CreateTextureOption.TextureHasAlphaChannel,
    has_mipmaps=QtQuick.QQuickWindow.CreateTextureOption.TextureHasMipmaps,
    owns_gl_texture=QtQuick.QQuickWindow.CreateTextureOption.TextureOwnsGLTexture,
    can_use_atlas=QtQuick.QQuickWindow.CreateTextureOption.TextureCanUseAtlas,
    is_opaque=QtQuick.QQuickWindow.CreateTextureOption.TextureIsOpaque,
)

RenderStageStr = Literal[
    "before_synchronizing",
    "after_synchronizing",
    "before_rendering",
    "after_rendering",
    "after_swap",
    "no_stage",
]

RENDER_STAGE: bidict[RenderStageStr, QtQuick.QQuickWindow.RenderStage] = bidict(
    before_synchronizing=QtQuick.QQuickWindow.RenderStage.BeforeSynchronizingStage,
    after_synchronizing=QtQuick.QQuickWindow.RenderStage.AfterSynchronizingStage,
    before_rendering=QtQuick.QQuickWindow.RenderStage.BeforeRenderingStage,
    after_rendering=QtQuick.QQuickWindow.RenderStage.AfterRenderingStage,
    after_swap=QtQuick.QQuickWindow.RenderStage.AfterSwapStage,
    no_stage=QtQuick.QQuickWindow.RenderStage.NoStage,
)

TextRenderTypeStr = Literal["qt_text", "native_text"]

TEXT_RENDER_TYPE: bidict[TextRenderTypeStr, QtQuick.QQuickWindow.TextRenderType] = bidict(
    qt_text=QtQuick.QQuickWindow.TextRenderType.QtTextRendering,
    native_text=QtQuick.QQuickWindow.TextRenderType.NativeTextRendering,
)


class QuickWindowMixin(gui.WindowMixin):
    def create_texture_from_image(self, image: gui.QImage, **kwargs):
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

    @classmethod
    def set_text_render_type(cls, typ: TextRenderTypeStr):
        """Set the default render type of text-like elements in Qt Quick.

        Note: setting the render type will only affect elements created afterwards;
        the render type of existing elements will not be modified.

        Args:
            typ: text render type to use
        """
        cls.setTextRenderType(TEXT_RENDER_TYPE.get_enum_value(typ))

    @classmethod
    def get_text_render_type(cls) -> TextRenderTypeStr:
        """Return the render type of text-like elements in Qt Quick.

        Returns:
            text render type
        """
        return TEXT_RENDER_TYPE.inverse[cls.textRenderType()]

    @contextlib.contextmanager
    def external_commands(self):
        self.beginExternalCommands()
        yield self
        self.endExternalCommands()

    def schedule_render_job(
        self,
        job: QtCore.QRunnable,
        render_stage: RenderStageStr | QtQuick.QQuickWindow.RenderStage,
    ):
        self.scheduleRenderJob(job, RENDER_STAGE.get_enum_value(render_stage))


class QuickWindow(QuickWindowMixin, QtQuick.QQuickWindow):
    """The window for displaying a graphical QML scene."""


if __name__ == "__main__":
    app = gui.app()
    wnd = QuickWindow()
    wnd.set_text_render_type("qt_text")
    img = gui.QImage()
    texture = wnd.create_texture_from_image(img)
