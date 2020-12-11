from qtpy import QtMultimedia

from prettyqt import core, multimedia, gui
from prettyqt.utils import bidict, InvalidParamError

FIELD_TYPES = bidict(
    progressive_frame=QtMultimedia.QVideoFrame.ProgressiveFrame,
    top_field=QtMultimedia.QVideoFrame.TopField,
    bottom_field=QtMultimedia.QVideoFrame.BottomField,
    interlaced_frame=QtMultimedia.QVideoFrame.InterlacedFrame,
)

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

HANDLE_TYPES = multimedia.abstractvideobuffer.HANDLE_TYPES
MAP_MODE = multimedia.abstractvideobuffer.MAP_MODE


class VideoFrame(QtMultimedia.QVideoFrame):
    def __repr__(self):
        return (
            f"VideoFrame({self.mappedBytes()}, {self.get_size()},"
            f"{self.bytesPerLine()}, {self.pixelFormat()})"
        )

    def get_handle_type(self) -> str:
        return HANDLE_TYPES.inverse[self.handleType()]

    def get_map_mode(self) -> str:
        return MAP_MODE.inverse[self.mapMode()]

    def get_size(self) -> core.Size:
        return core.Size(self.size())

    def get_image(self) -> gui.Image:
        return gui.Image(self.image())

    def get_pixel_format(self) -> str:
        return PIXEL_FORMAT.inverse[self.pixelFormat()]

    def get_field_type(self) -> str:
        """Set field type.

        Valid values: "progressive_frame", "top_field", "bottom_field",
                      "interlaced_frame"

        """
        return FIELD_TYPES.inverse[self.fieldType()]

    def set_field_type(self, typ: str):
        """Return current field type.

        Possible values: "progressive_frame", "top_field", "bottom_field",
                         "interlaced_frame"
        Args:
            typ: capture mode

        Raises:
            InvalidParamError: capture mode does not exist
        """
        if typ not in FIELD_TYPES:
            raise InvalidParamError(typ, FIELD_TYPES)
        self.setFieldType(FIELD_TYPES[typ])


if __name__ == "__main__":
    frame = VideoFrame()
