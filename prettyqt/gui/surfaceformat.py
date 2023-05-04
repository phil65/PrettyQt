from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict, get_repr


# COLOR_SPACE = bidict(
#     default=QtGui.QSurfaceFormat.ColorSpace.DefaultColorSpace,
#     srgb=QtGui.QSurfaceFormat.ColorSpace.sRGBColorSpace,
# )

# ColorSpaceStr = Literal["default", "srgb"]

FORMAT_OPTION = bidict(
    stereo_buffers=QtGui.QSurfaceFormat.FormatOption.StereoBuffers,
    debug_context=QtGui.QSurfaceFormat.FormatOption.DebugContext,
    deprecated_functions=QtGui.QSurfaceFormat.FormatOption.DeprecatedFunctions,
    reset_notification=QtGui.QSurfaceFormat.FormatOption.ResetNotification,
    protected_content=QtGui.QSurfaceFormat.FormatOption.ProtectedContent,
)

FormatOptionStr = Literal[
    "stereo_buffers",
    "debug_context",
    "deprecated_functions",
    "reset_notification",
    "protected_content",
]

OPEN_GL_CONTEXT_PROFILE = bidict(
    none=QtGui.QSurfaceFormat.OpenGLContextProfile.NoProfile,
    core=QtGui.QSurfaceFormat.OpenGLContextProfile.CoreProfile,
    compatibility=QtGui.QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile,
)

OpenGLContextProfileStr = Literal["none", "core", "compatibility"]

RENDERABLE_TYPE = bidict(
    default=QtGui.QSurfaceFormat.RenderableType.DefaultRenderableType,
    open_gl=QtGui.QSurfaceFormat.RenderableType.OpenGL,
    open_gl_es=QtGui.QSurfaceFormat.RenderableType.OpenGLES,
    open_vg=QtGui.QSurfaceFormat.RenderableType.OpenVG,
)

RenderableTypeStr = Literal["default", "open_gl", "open_gl_es", "open_vg"]

SWAP_BEHAVIOR = bidict(
    default=QtGui.QSurfaceFormat.SwapBehavior.DefaultSwapBehavior,
    single=QtGui.QSurfaceFormat.SwapBehavior.SingleBuffer,
    double=QtGui.QSurfaceFormat.SwapBehavior.DoubleBuffer,
    triple=QtGui.QSurfaceFormat.SwapBehavior.TripleBuffer,
)

SwapBehaviorStr = Literal["default", "single", "double", "triple"]


class SurfaceFormatMixin:
    def __repr__(self):
        return get_repr(self)

    def get_profile(self) -> OpenGLContextProfileStr:
        """Get the current OpenGl profile.

        Returns:
            OpenGL profile
        """
        return OPEN_GL_CONTEXT_PROFILE.inverse[self.profile()]

    def get_renderable_type(self) -> RenderableTypeStr:
        """Get the current renderable type.

        Returns:
            renderable type
        """
        return RENDERABLE_TYPE.inverse[self.renderableType()]

    def get_swap_behavior(self) -> SwapBehaviorStr:
        """Get the current swap behavior.

        Returns:
            swap behavior
        """
        return SWAP_BEHAVIOR.inverse[self.swapBehavior()]


class SurfaceFormat(SurfaceFormatMixin, QtGui.QSurfaceFormat):
    pass
