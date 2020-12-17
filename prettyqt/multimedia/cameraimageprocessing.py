from typing import Literal

from qtpy import QtMultimedia

from prettyqt import core, multimedia
from prettyqt.utils import InvalidParamError, bidict


COLOR_FILTERS = bidict(
    none=QtMultimedia.QCameraImageProcessing.ColorFilterNone,
    grayscale=QtMultimedia.QCameraImageProcessing.ColorFilterGrayscale,
    negative=QtMultimedia.QCameraImageProcessing.ColorFilterNegative,
    solarize=QtMultimedia.QCameraImageProcessing.ColorFilterSolarize,
    sepia=QtMultimedia.QCameraImageProcessing.ColorFilterSepia,
    posterize=QtMultimedia.QCameraImageProcessing.ColorFilterPosterize,
    whiteboard=QtMultimedia.QCameraImageProcessing.ColorFilterWhiteboard,
    blackboard=QtMultimedia.QCameraImageProcessing.ColorFilterBlackboard,
    aqua=QtMultimedia.QCameraImageProcessing.ColorFilterAqua,
    vendor=QtMultimedia.QCameraImageProcessing.ColorFilterVendor,
)

ColorFilterStr = Literal[
    "none",
    "grayscale",
    "negative",
    "solarize",
    "sepia",
    "posterize",
    "whiteboard",
    "blackboard",
    "aqua",
    "vendor",
]

WHITE_BALANCE_MODE = bidict(
    auto=QtMultimedia.QCameraImageProcessing.WhiteBalanceAuto,
    manual=QtMultimedia.QCameraImageProcessing.WhiteBalanceManual,
    sunlight=QtMultimedia.QCameraImageProcessing.WhiteBalanceSunlight,
    cloudy=QtMultimedia.QCameraImageProcessing.WhiteBalanceCloudy,
    shade=QtMultimedia.QCameraImageProcessing.WhiteBalanceShade,
    tungsten=QtMultimedia.QCameraImageProcessing.WhiteBalanceTungsten,
    fluorescent=QtMultimedia.QCameraImageProcessing.WhiteBalanceFluorescent,
    flash=QtMultimedia.QCameraImageProcessing.WhiteBalanceFlash,
    sunset=QtMultimedia.QCameraImageProcessing.WhiteBalanceSunset,
    vendor=QtMultimedia.QCameraImageProcessing.WhiteBalanceVendor,
)

WhiteBalanceModeStr = Literal[
    "auto",
    "manual",
    "sunlight",
    "cloudy",
    "shade",
    "tungsten",
    "fluorescent",
    "flash",
    "sunset",
    "vendor",
]

QtMultimedia.QCameraImageProcessing.__bases__ = (core.Object,)


class CameraImageProcessing(core.Object):
    def __init__(self, item: QtMultimedia.QCameraImageProcessing):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_color_filter(self, mode: ColorFilterStr):
        """Set the color filter.

        Args:
            mode: color filter

        Raises:
            InvalidParamError: color filter does not exist
        """
        if mode not in COLOR_FILTERS:
            raise InvalidParamError(mode, COLOR_FILTERS)
        self.item.setColorFilter(COLOR_FILTERS[mode])

    def get_color_filter(self) -> ColorFilterStr:
        """Return current exposure mode.

        Returns:
            color filter
        """
        return COLOR_FILTERS.inverse[self.item.colorFilter()]

    def set_white_balance_mode(self, mode: WhiteBalanceModeStr):
        """Set the white balance mode.

        Args:
            mode: white balance mode

        Raises:
            InvalidParamError: white balance mode does not exist
        """
        if mode not in WHITE_BALANCE_MODE:
            raise InvalidParamError(mode, WHITE_BALANCE_MODE)
        self.item.setWhiteBalanceMode(WHITE_BALANCE_MODE[mode])

    def get_white_balance_mode(self) -> WhiteBalanceModeStr:
        """Return current white balance mode.

        Returns:
            white balance mode
        """
        return WHITE_BALANCE_MODE.inverse[self.item.whiteBalanceMode()]

    def is_color_filter_supported(self, filter_: ColorFilterStr) -> bool:
        if filter_ not in COLOR_FILTERS:
            raise InvalidParamError(filter_, COLOR_FILTERS)
        return self.item.isColorFilterSupported(COLOR_FILTERS[filter_])

    def is_white_balance_mode_supported(self, mode: WhiteBalanceModeStr) -> bool:
        if mode not in WHITE_BALANCE_MODE:
            raise InvalidParamError(mode, WHITE_BALANCE_MODE)
        return self.item.isWhiteBalanceModeSupported(WHITE_BALANCE_MODE[mode])


if __name__ == "__main__":
    cam = multimedia.Camera()
    focus = cam.get_focus()
