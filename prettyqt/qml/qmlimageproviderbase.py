from qtpy import QtQml

from prettyqt.utils import bidict


FLAGS = bidict(
    force_async_image_loading=QtQml.QQmlImageProviderBase.ForceAsynchronousImageLoading,
)


IMAGE_TYPE = bidict(
    image=QtQml.QQmlImageProviderBase.Image,
    pixmap=QtQml.QQmlImageProviderBase.Pixmap,
    texture=QtQml.QQmlImageProviderBase.Texture,
    image_response=QtQml.QQmlImageProviderBase.ImageResponse,
)


class QmlImageProviderBase(QtQml.QQmlImageProviderBase):
    pass
