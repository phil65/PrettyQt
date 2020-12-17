from typing import Literal, Union

from qtpy import QtMultimedia

from prettyqt.utils import bidict


HANDLE_TYPE = bidict(
    none=QtMultimedia.QAbstractVideoBuffer.NoHandle,
    gl_texture=QtMultimedia.QAbstractVideoBuffer.GLTextureHandle,
    xv_shm_image=QtMultimedia.QAbstractVideoBuffer.XvShmImageHandle,
    core_image=QtMultimedia.QAbstractVideoBuffer.CoreImageHandle,
    pixmap=QtMultimedia.QAbstractVideoBuffer.QPixmapHandle,
    egl_image=QtMultimedia.QAbstractVideoBuffer.EGLImageHandle,
    user=QtMultimedia.QAbstractVideoBuffer.UserHandle,
)

HandleTypeStr = Literal[
    "none", "gl_texture", "xv_shm_image", "core_image", "pixmap", "egl_image", "user"
]

MAP_MODE = bidict(
    not_mapped=QtMultimedia.QAbstractVideoBuffer.NotMapped,
    read_only=QtMultimedia.QAbstractVideoBuffer.ReadOnly,
    write_only=QtMultimedia.QAbstractVideoBuffer.WriteOnly,
    read_write=QtMultimedia.QAbstractVideoBuffer.ReadWrite,
)

MapModeStr = Literal["not_mapped", "read_only", "write_only", "read_write"]


class AbstractVideoBuffer(QtMultimedia.QAbstractVideoBuffer):
    def __init__(self, handle_type: Union[int, str]):
        if handle_type in HANDLE_TYPE:
            handle_type = HANDLE_TYPE[handle_type]
        super().__init__(handle_type)

    def __repr__(self):
        return f"{type(self).__name__}({self.get_handle_type()!r})"

    def get_handle_type(self) -> HandleTypeStr:
        """Return current handle type.

        Returns:
            handle type
        """
        return HANDLE_TYPE.inverse[self.handleType()]

    def get_map_mode(self) -> MapModeStr:
        """Return current map mode.

        Returns:
            map mode
        """
        return MAP_MODE.inverse[self.mapMode()]

    def map_planes(
        self,
        mode: Union[int, str],
        num_bytes: int,
        bytes_per_line: int = 4,
        data: int = 4,
    ):
        if mode in MAP_MODE:
            mode = MAP_MODE[mode]
        self.mapPlanes(mode, num_bytes, bytes_per_line, data)

    def map(
        self,
        mode: Union[int, str],
        num_bytes: int,
        bytes_per_line: int = 4,
    ):
        if mode in MAP_MODE:
            mode = MAP_MODE[mode]
        super().map(mode, num_bytes, bytes_per_line)
