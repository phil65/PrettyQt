from typing import Literal

from qtpy import QtMultimedia

from prettyqt import core, gui, multimedia
from prettyqt.utils import InvalidParamError, bidict


FIELD_TYPE = bidict(
    progressive_frame=QtMultimedia.QVideoFrame.ProgressiveFrame,
    top_field=QtMultimedia.QVideoFrame.TopField,
    bottom_field=QtMultimedia.QVideoFrame.BottomField,
    interlaced_frame=QtMultimedia.QVideoFrame.InterlacedFrame,
)

FieldTypeStr = Literal[
    "progressive_frame", "top_field", "bottom_field", "interlaced_frame"
]

PIXEL_FORMAT = bidict(
    invalid=QtMultimedia.QVideoFrame.Format_Invalid,
    argb32=QtMultimedia.QVideoFrame.Format_ARGB32,
    argb32_premultiplied=QtMultimedia.QVideoFrame.Format_ARGB32_Premultiplied,
    rgb32=QtMultimedia.QVideoFrame.Format_RGB32,
    rgb24=QtMultimedia.QVideoFrame.Format_RGB24,
    rgb565=QtMultimedia.QVideoFrame.Format_RGB565,
    rgb555=QtMultimedia.QVideoFrame.Format_RGB555,
    argb8565_premultiplied=QtMultimedia.QVideoFrame.Format_ARGB8565_Premultiplied,
    bgra32=QtMultimedia.QVideoFrame.Format_BGRA32,
    bgra32_premultiplied=QtMultimedia.QVideoFrame.Format_BGRA32_Premultiplied,
    abgr32=QtMultimedia.QVideoFrame.Format_ABGR32,
    bgr32=QtMultimedia.QVideoFrame.Format_BGR32,
    bgr24=QtMultimedia.QVideoFrame.Format_BGR24,
    bgr565=QtMultimedia.QVideoFrame.Format_BGR565,
    bgr555=QtMultimedia.QVideoFrame.Format_BGR555,
    bgra5658_premultiplied=QtMultimedia.QVideoFrame.Format_BGRA5658_Premultiplied,
    ayuv444=QtMultimedia.QVideoFrame.Format_AYUV444,
    yuv444_premultiplied=QtMultimedia.QVideoFrame.Format_AYUV444_Premultiplied,
    yuv444=QtMultimedia.QVideoFrame.Format_YUV444,
    yuv420p=QtMultimedia.QVideoFrame.Format_YUV420P,
    yuv422p=QtMultimedia.QVideoFrame.Format_YUV422P,
    yv12=QtMultimedia.QVideoFrame.Format_YV12,
    uyvy=QtMultimedia.QVideoFrame.Format_UYVY,
    yuyv=QtMultimedia.QVideoFrame.Format_YUYV,
    nv12=QtMultimedia.QVideoFrame.Format_NV12,
    nv21=QtMultimedia.QVideoFrame.Format_NV21,
    imc1=QtMultimedia.QVideoFrame.Format_IMC1,
    imc2=QtMultimedia.QVideoFrame.Format_IMC2,
    imc3=QtMultimedia.QVideoFrame.Format_IMC3,
    imc4=QtMultimedia.QVideoFrame.Format_IMC4,
    y8=QtMultimedia.QVideoFrame.Format_Y8,
    y16=QtMultimedia.QVideoFrame.Format_Y16,
    jpeg=QtMultimedia.QVideoFrame.Format_Jpeg,
    camera_raw=QtMultimedia.QVideoFrame.Format_CameraRaw,
    adobe_dng=QtMultimedia.QVideoFrame.Format_AdobeDng,
    user=QtMultimedia.QVideoFrame.Format_User,
)

PixelFormatStr = Literal[
    "invalid",
    "argb32",
    "argb32_premultiplied",
    "rgb32",
    "rgb24",
    "rgb565",
    "rgb555",
    "argb8565_premultiplied",
    "bgra32",
    "bgra32_premultiplied",
    "abgr32",
    "bgr32",
    "bgr24",
    "bgr565",
    "bgr555",
    "bgra5658_premultiplied",
    "ayuv444",
    "yuv444_premultiplied",
    "yuv444",
    "yuv420p",
    "yuv422p",
    "yv12",
    "uyvy",
    "yuyv",
    "nv12",
    "nv21",
    "imc1",
    "imc2",
    "imc3",
    "imc4",
    "y8",
    "y16",
    "jpeg",
    "camera_raw",
    "adobe_dng",
    "user",
]


class VideoFrame(QtMultimedia.QVideoFrame):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.mappedBytes()}, {self.get_size()},"
            f"{self.bytesPerLine()}, {self.pixelFormat()})"
        )

    def get_handle_type(self) -> multimedia.abstractvideobuffer.HandleTypeStr:
        return multimedia.abstractvideobuffer.HANDLE_TYPE.inverse[self.handleType()]

    def get_map_mode(self) -> multimedia.abstractvideobuffer.MapModeStr:
        return multimedia.abstractvideobuffer.MAP_MODE.inverse[self.mapMode()]

    def get_size(self) -> core.Size:
        return core.Size(self.size())

    def get_image(self) -> gui.Image:
        return gui.Image(self.image())

    def get_pixel_format(self) -> PixelFormatStr:
        return PIXEL_FORMAT.inverse[self.pixelFormat()]

    def get_field_type(self) -> FieldTypeStr:
        """Get field type.

        Returns:
            Field type
        """
        return FIELD_TYPE.inverse[self.fieldType()]

    def set_field_type(self, typ: FieldTypeStr):
        """Set current field type.

        Args:
            typ: capture mode

        Raises:
            InvalidParamError: capture mode does not exist
        """
        if typ not in FIELD_TYPE:
            raise InvalidParamError(typ, FIELD_TYPE)
        self.setFieldType(FIELD_TYPE[typ])


if __name__ == "__main__":
    frame = VideoFrame()
