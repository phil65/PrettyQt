from __future__ import annotations

from prettyqt.qt import QtQml
from prettyqt.utils import bidict


mod = QtQml.QQmlImageProviderBase

FLAGS = bidict(
    force_async_image_loading=mod.Flag.ForceAsynchronousImageLoading,
)


IMAGE_TYPE = bidict(
    image=mod.ImageType.Image,
    pixmap=mod.ImageType.Pixmap,
    texture=mod.ImageType.Texture,
    image_response=mod.ImageType.ImageResponse,
)


class QmlImageProviderBase(QtQml.QQmlImageProviderBase):
    pass
