from typing import TYPE_CHECKING, Literal

from prettyqt.qt import QtQml
from prettyqt.utils import bidict


mod = QtQml.QQmlImageProviderBase

FlagsStr = Literal["force_async_image_loading"]

FLAGS: bidict[FlagsStr, mod.Flag] = bidict(
    force_async_image_loading=mod.Flag.ForceAsynchronousImageLoading,
)

ImageTypeStr = Literal["image", "pixmap", "texture", "image_response", "invalid"]

IMAGE_TYPE: bidict[ImageTypeStr, mod.ImageType] = bidict(
    image=mod.ImageType.Image,
    pixmap=mod.ImageType.Pixmap,
    texture=mod.ImageType.Texture,
    image_response=mod.ImageType.ImageResponse,
)
if hasattr(mod.ImageType, "Invalid"):
    IMAGE_TYPE["invalid"] = mod.ImageType.Invalid


if TYPE_CHECKING:
    _QmlImageProviderBaseBase = QtQml.QQmlImageProviderBase
else:
    _QmlImageProviderBaseBase = object


class QmlImageProviderBaseMixin(_QmlImageProviderBaseBase):
    pass


class QmlImageProviderBase(QmlImageProviderBaseMixin, QtQml.QQmlImageProviderBase):
    """Used to register image providers in the QML engine."""
