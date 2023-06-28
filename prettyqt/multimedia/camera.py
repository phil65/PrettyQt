from __future__ import annotations

from typing import Literal

from prettyqt import core, multimedia
from prettyqt.utils import bidict


ErrorStr = Literal["none", "camera"]

ERROR: bidict[ErrorStr, multimedia.QCamera.Error] = bidict(
    none=multimedia.QCamera.Error.NoError,
    camera=multimedia.QCamera.Error.CameraError,
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

EXPOSURE_MODE: bidict[ExposureModeStr, multimedia.QCamera.ExposureMode] = bidict(
    auto=multimedia.QCamera.ExposureMode.ExposureAuto,
    manual=multimedia.QCamera.ExposureMode.ExposureManual,
    portrait=multimedia.QCamera.ExposureMode.ExposurePortrait,
    night=multimedia.QCamera.ExposureMode.ExposureNight,
    sports=multimedia.QCamera.ExposureMode.ExposureSports,
    snow=multimedia.QCamera.ExposureMode.ExposureSnow,
    beach=multimedia.QCamera.ExposureMode.ExposureBeach,
    action=multimedia.QCamera.ExposureMode.ExposureAction,
    landscape=multimedia.QCamera.ExposureMode.ExposureLandscape,
    night_portrait=multimedia.QCamera.ExposureMode.ExposureNightPortrait,
    threatre=multimedia.QCamera.ExposureMode.ExposureTheatre,
    sunset=multimedia.QCamera.ExposureMode.ExposureSunset,
    steady_photo=multimedia.QCamera.ExposureMode.ExposureSteadyPhoto,
    fireworks=multimedia.QCamera.ExposureMode.ExposureFireworks,
    party=multimedia.QCamera.ExposureMode.ExposureParty,
    candle_light=multimedia.QCamera.ExposureMode.ExposureCandlelight,
    barcode=multimedia.QCamera.ExposureMode.ExposureBarcode,
)

FeatureStr = Literal[
    "color_temperature",
    "exposure_compensation",
    "iso_sensitivity",
    "manual_exposure_time",
    "custom_focus_point",
    "focus_distance",
]

FEATURE: bidict[FeatureStr, multimedia.QCamera.Feature] = bidict(
    none=multimedia.QCamera.Feature(0),
    color_temperature=multimedia.QCamera.Feature.ColorTemperature,
    exposure_compensation=multimedia.QCamera.Feature.ExposureCompensation,
    iso_sensitivity=multimedia.QCamera.Feature.IsoSensitivity,
    manual_exposure_time=multimedia.QCamera.Feature.ManualExposureTime,
    custom_focus_point=multimedia.QCamera.Feature.CustomFocusPoint,
    focus_distance=multimedia.QCamera.Feature.FocusDistance,
)

FlashModeStr = Literal["off", "on", "auto"]

FLASH_MODE: bidict[FlashModeStr, multimedia.QCamera.FlashMode] = bidict(
    off=multimedia.QCamera.FlashMode.FlashOff,
    on=multimedia.QCamera.FlashMode.FlashOn,
    auto=multimedia.QCamera.FlashMode.FlashAuto,
)

FocusModeStr = Literal[
    "auto",
    "auto_near",
    "auto_far",
    "focal",
    "infinity",
    "manual",
]

FOCUS_MODE: bidict[FocusModeStr, multimedia.QCamera.FocusMode] = bidict(
    auto=multimedia.QCamera.FocusMode.FocusModeAuto,
    auto_near=multimedia.QCamera.FocusMode.FocusModeAutoNear,
    auto_far=multimedia.QCamera.FocusMode.FocusModeAutoFar,
    focal=multimedia.QCamera.FocusMode.FocusModeHyperfocal,
    infinity=multimedia.QCamera.FocusMode.FocusModeInfinity,
    manual=multimedia.QCamera.FocusMode.FocusModeManual,
)

TorchModeStr = Literal["off", "on", "auto"]

TORCH_MODE: bidict[TorchModeStr, multimedia.QCamera.TorchMode] = bidict(
    off=multimedia.QCamera.TorchMode.TorchOff,
    on=multimedia.QCamera.TorchMode.TorchOn,
    auto=multimedia.QCamera.TorchMode.TorchAuto,
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
    WhiteBalanceModeStr, multimedia.QCamera.WhiteBalanceMode
] = bidict(
    auto=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceAuto,
    manual=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceManual,
    sunlight=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceSunlight,
    cloudy=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceCloudy,
    shade=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceShade,
    tungsten=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceTungsten,
    fluorescent=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceFluorescent,
    flash=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceFlash,
    sunset=multimedia.QCamera.WhiteBalanceMode.WhiteBalanceSunset,
)


class Camera(core.ObjectMixin, multimedia.QCamera):
    def set_exposure_mode(
        self, mode: ExposureModeStr | multimedia.QCamera.ExposureMode
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

    def set_torch_mode(self, mode: TorchModeStr | multimedia.QCamera.TorchMode):
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

    def set_flash_mode(self, mode: FlashModeStr | multimedia.QCamera.FlashMode):
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
        self, mode: WhiteBalanceModeStr | multimedia.QCamera.WhiteBalanceMode
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
