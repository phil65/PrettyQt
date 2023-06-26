from __future__ import annotations

from typing import Literal

from prettyqt import core, multimedia
from prettyqt.qt import QtMultimedia
from prettyqt.utils import bidict


ErrorStr = Literal["none", "camera"]

ERROR: bidict[ErrorStr, QtMultimedia.QCamera.Error] = bidict(
    none=QtMultimedia.QCamera.Error.NoError,
    camera=QtMultimedia.QCamera.Error.CameraError,
)

ExposureModeStr = Literal[
    "auto",
    "manual",
    "portrait",
    "night",
    "sports",
    "snow",
    "beach",
    "action",
    "landscape",
    "night_portrait",
    "threatre",
    "sunset",
    "steady_photo",
    "fireworks",
    "party",
    "candle_light",
    "barcode",
]

EXPOSURE_MODE: bidict[ExposureModeStr, QtMultimedia.QCamera.ExposureMode] = bidict(
    auto=QtMultimedia.QCamera.ExposureMode.ExposureAuto,
    manual=QtMultimedia.QCamera.ExposureMode.ExposureManual,
    portrait=QtMultimedia.QCamera.ExposureMode.ExposurePortrait,
    night=QtMultimedia.QCamera.ExposureMode.ExposureNight,
    sports=QtMultimedia.QCamera.ExposureMode.ExposureSports,
    snow=QtMultimedia.QCamera.ExposureMode.ExposureSnow,
    beach=QtMultimedia.QCamera.ExposureMode.ExposureBeach,
    action=QtMultimedia.QCamera.ExposureMode.ExposureAction,
    landscape=QtMultimedia.QCamera.ExposureMode.ExposureLandscape,
    night_portrait=QtMultimedia.QCamera.ExposureMode.ExposureNightPortrait,
    threatre=QtMultimedia.QCamera.ExposureMode.ExposureTheatre,
    sunset=QtMultimedia.QCamera.ExposureMode.ExposureSunset,
    steady_photo=QtMultimedia.QCamera.ExposureMode.ExposureSteadyPhoto,
    fireworks=QtMultimedia.QCamera.ExposureMode.ExposureFireworks,
    party=QtMultimedia.QCamera.ExposureMode.ExposureParty,
    candle_light=QtMultimedia.QCamera.ExposureMode.ExposureCandlelight,
    barcode=QtMultimedia.QCamera.ExposureMode.ExposureBarcode,
)

FeatureStr = Literal[
    "color_temperature",
    "exposure_compensation",
    "iso_sensitivity",
    "manual_exposure_time",
    "custom_focus_point",
    "focus_distance",
]

FEATURE: bidict[FeatureStr, QtMultimedia.QCamera.Feature] = bidict(
    none=QtMultimedia.QCamera.Feature(0),
    color_temperature=QtMultimedia.QCamera.Feature.ColorTemperature,
    exposure_compensation=QtMultimedia.QCamera.Feature.ExposureCompensation,
    iso_sensitivity=QtMultimedia.QCamera.Feature.IsoSensitivity,
    manual_exposure_time=QtMultimedia.QCamera.Feature.ManualExposureTime,
    custom_focus_point=QtMultimedia.QCamera.Feature.CustomFocusPoint,
    focus_distance=QtMultimedia.QCamera.Feature.FocusDistance,
)

FlashModeStr = Literal["off", "on", "auto"]

FLASH_MODE: bidict[FlashModeStr, QtMultimedia.QCamera.FlashMode] = bidict(
    off=QtMultimedia.QCamera.FlashMode.FlashOff,
    on=QtMultimedia.QCamera.FlashMode.FlashOn,
    auto=QtMultimedia.QCamera.FlashMode.FlashAuto,
)

FocusModeStr = Literal[
    "auto",
    "auto_near",
    "auto_far",
    "focal",
    "infinity",
    "manual",
]

FOCUS_MODE: bidict[FocusModeStr, QtMultimedia.QCamera.FocusMode] = bidict(
    auto=QtMultimedia.QCamera.FocusMode.FocusModeAuto,
    auto_near=QtMultimedia.QCamera.FocusMode.FocusModeAutoNear,
    auto_far=QtMultimedia.QCamera.FocusMode.FocusModeAutoFar,
    focal=QtMultimedia.QCamera.FocusMode.FocusModeHyperfocal,
    infinity=QtMultimedia.QCamera.FocusMode.FocusModeInfinity,
    manual=QtMultimedia.QCamera.FocusMode.FocusModeManual,
)

TorchModeStr = Literal["off", "on", "auto"]

TORCH_MODE: bidict[TorchModeStr, QtMultimedia.QCamera.TorchMode] = bidict(
    off=QtMultimedia.QCamera.TorchMode.TorchOff,
    on=QtMultimedia.QCamera.TorchMode.TorchOn,
    auto=QtMultimedia.QCamera.TorchMode.TorchAuto,
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
]

WHITE_BALANCE: bidict[
    WhiteBalanceModeStr, QtMultimedia.QCamera.WhiteBalanceMode
] = bidict(
    auto=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceAuto,
    manual=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceManual,
    sunlight=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceSunlight,
    cloudy=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceCloudy,
    shade=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceShade,
    tungsten=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceTungsten,
    fluorescent=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceFluorescent,
    flash=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceFlash,
    sunset=QtMultimedia.QCamera.WhiteBalanceMode.WhiteBalanceSunset,
)


class Camera(core.ObjectMixin, QtMultimedia.QCamera):
    def set_exposure_mode(
        self, mode: ExposureModeStr | QtMultimedia.QCamera.ExposureMode
    ):
        """Set the exposure mode.

        Args:
            mode: exposure mode
        """
        self.setExposureMode(EXPOSURE_MODE.get_enum_value(mode))

    def get_exposure_mode(self) -> ExposureModeStr:
        """Return current exposure mode.

        Returns:
            exposure mode
        """
        return EXPOSURE_MODE.inverse[self.exposureMode()]

    def set_torch_mode(self, mode: TorchModeStr | QtMultimedia.QCamera.TorchMode):
        """Set the torch mode.

        Args:
            mode: torch mode
        """
        self.setTorchMode(TORCH_MODE.get_enum_value(mode))

    def get_torch_mode(self) -> TorchModeStr:
        """Return current torch mode.

        Returns:
            torch mode
        """
        return TORCH_MODE.inverse[self.torchMode()]

    def set_flash_mode(self, mode: FlashModeStr | QtMultimedia.QCamera.FlashMode):
        """Set the flash mode.

        Args:
            mode: flash mode
        """
        self.setFlashMode(FLASH_MODE.get_enum_value(mode))

    def get_flash_mode(self) -> FlashModeStr:
        """Return current flash mode.

        Returns:
            flash mode
        """
        return FLASH_MODE.inverse[self.flashMode()]

    def set_white_balance_mode(
        self, mode: WhiteBalanceModeStr | QtMultimedia.QCamera.WhiteBalanceMode
    ):
        """Set the white balance mode.

        Args:
            mode: white balance mode
        """
        self.setWhiteBalanceMode(WHITE_BALANCE.get_enum_value(mode))

    def get_white_balance_mode(self) -> WhiteBalanceModeStr:
        """Return current white balance mode.

        Returns:
            white balance mode
        """
        return WHITE_BALANCE.inverse[self.whiteBalanceMode()]

    def get_supported_features(self) -> list[FeatureStr]:
        return FEATURE.get_list(self.supportedFeatures())

    def get_error(self) -> ErrorStr:
        """Return current error state.

        Returns:
            error state
        """
        return ERROR.inverse[self.error()]

    def get_camera_format(self) -> multimedia.CameraFormat:
        return multimedia.CameraFormat(self.cameraFormat())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    cam = Camera()
    cam.supportedFeatures()
    print(type(cam.supportedFeatures()).mro())
