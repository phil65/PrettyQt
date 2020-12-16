from qtpy import QtMultimedia

from prettyqt import core, multimedia
from prettyqt.utils import bidict, InvalidParamError, mappers


EXPOSURE_MODES = bidict(
    auto=QtMultimedia.QCameraExposure.ExposureAuto,
    manual=QtMultimedia.QCameraExposure.ExposureManual,
    portrait=QtMultimedia.QCameraExposure.ExposurePortrait,
    night=QtMultimedia.QCameraExposure.ExposureNight,
    backlight=QtMultimedia.QCameraExposure.ExposureBacklight,
    spotlight=QtMultimedia.QCameraExposure.ExposureSpotlight,
    sports=QtMultimedia.QCameraExposure.ExposureSports,
    snow=QtMultimedia.QCameraExposure.ExposureSnow,
    beach=QtMultimedia.QCameraExposure.ExposureBeach,
    large_aperture=QtMultimedia.QCameraExposure.ExposureLargeAperture,
    small_aperture=QtMultimedia.QCameraExposure.ExposureSmallAperture,
    action=QtMultimedia.QCameraExposure.ExposureAction,
    landscape=QtMultimedia.QCameraExposure.ExposureLandscape,
    night_portrait=QtMultimedia.QCameraExposure.ExposureNightPortrait,
    theatre=QtMultimedia.QCameraExposure.ExposureTheatre,
    sunset=QtMultimedia.QCameraExposure.ExposureSunset,
    steady_photo=QtMultimedia.QCameraExposure.ExposureSteadyPhoto,
    fireworks=QtMultimedia.QCameraExposure.ExposureFireworks,
    party=QtMultimedia.QCameraExposure.ExposureParty,
    candlelight=QtMultimedia.QCameraExposure.ExposureCandlelight,
    barcode=QtMultimedia.QCameraExposure.ExposureBarcode,
    mode_vendor=QtMultimedia.QCameraExposure.ExposureModeVendor,
)

FLASH_MODES = mappers.FlagMap(
    QtMultimedia.QCameraExposure.FlashModes,
    auto=QtMultimedia.QCameraExposure.FlashAuto,
    flash_off=QtMultimedia.QCameraExposure.FlashOff,
    flash_on=QtMultimedia.QCameraExposure.FlashOn,
    red_eye_reduction=QtMultimedia.QCameraExposure.FlashRedEyeReduction,
    fill=QtMultimedia.QCameraExposure.FlashFill,
    torch=QtMultimedia.QCameraExposure.FlashTorch,
    video_light=QtMultimedia.QCameraExposure.FlashVideoLight,
    sync_front_curtain=QtMultimedia.QCameraExposure.FlashSlowSyncFrontCurtain,
    sync_rear_curtain=QtMultimedia.QCameraExposure.FlashSlowSyncRearCurtain,
    manual=QtMultimedia.QCameraExposure.FlashManual,
)

METERING_MODES = bidict(
    matrix=QtMultimedia.QCameraExposure.MeteringMatrix,
    average=QtMultimedia.QCameraExposure.MeteringAverage,
    spot=QtMultimedia.QCameraExposure.MeteringSpot,
)

QtMultimedia.QCameraExposure.__bases__ = (core.Object,)


class CameraExposure(core.Object):
    def __init__(self, item: QtMultimedia.QCameraExposure):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def set_exposure_mode(self, mode: str):
        """Set the exposure mode.

        Allowed values are "auto", "manual", "portrait", "night", "backlight",
                           "spotlight", "sports", "snow", "beach", "large_aperture",
                           "small_aperture", "action", "landscape", "night_portrait",
                           "theatre", "sunset", "steady_photo", "fireworks", "party",
                           "candlelight", "barcode", "mode_vendor"

        Args:
            mode: exposure mode

        Raises:
            InvalidParamError: exposure mode does not exist
        """
        if mode not in EXPOSURE_MODES:
            raise InvalidParamError(mode, EXPOSURE_MODES)
        self.item.setExposureMode(EXPOSURE_MODES[mode])

    def get_exposure_mode(self) -> str:
        """Return current exposure mode.

        Possible values: "auto", "manual", "portrait", "night", "backlight",
                         "spotlight", "sports", "snow", "beach", "large_aperture",
                         "small_aperture", "action", "landscape", "night_portrait",
                         "theatre", "sunset", "steady_photo", "fireworks", "party",
                         "candlelight", "barcode", "mode_vendor"

        Returns:
            exposure mode
        """
        return EXPOSURE_MODES.inverse[self.item.exposureMode()]

    def set_flash_mode(self, mode: str):
        """Set the flash mode.

        Allowed values are "auto", "flash_on", "flash_off", "red_eye_reduction",
                           "fill", "torch", "video_light", "sync_front_curtain",
                           "sync_rear_curtain", "manual"

        Args:
            mode: flash mode

        Raises:
            InvalidParamError: flash mode does not exist
        """
        if mode not in FLASH_MODES:
            raise InvalidParamError(mode, FLASH_MODES)
        self.item.setFlashMode(FLASH_MODES[mode])

    def get_flash_mode(self) -> str:
        """Return current flash mode.

        Possible values: "auto", "flash_on", "flash_off", "red_eye_reduction",
                         "fill", "torch", "video_light", "sync_front_curtain",
                         "sync_rear_curtain", "manual"

        Returns:
            flash mode
        """
        return FLASH_MODES.inverse[self.item.flashMode()]

    def set_metering_mode(self, mode: str):
        """Set the metering mode.

        Allowed values are "matrix", "average", "spot"

        Args:
            mode: metering mode

        Raises:
            InvalidParamError: metering mode does not exist
        """
        if mode not in METERING_MODES:
            raise InvalidParamError(mode, METERING_MODES)
        self.item.setMeteringMode(METERING_MODES[mode])

    def get_metering_mode(self) -> str:
        """Return current metering mode.

        Possible values: "matrix", "average", "spot"

        Returns:
            metering mode
        """
        return METERING_MODES.inverse[self.item.meteringMode()]

    def get_spot_metering_point(self) -> core.PointF:
        return core.PointF(self.item.spotMeteringPoint())

    def is_exposure_mode_supported(self, mode: str) -> bool:
        if mode not in EXPOSURE_MODES:
            raise InvalidParamError(mode, EXPOSURE_MODES)
        return self.item.isExposureModeSupported(EXPOSURE_MODES[mode])

    def is_flash_mode_supported(self, mode: str) -> bool:
        if mode not in FLASH_MODES:
            raise InvalidParamError(mode, FLASH_MODES)
        return self.item.isFlashModeSupported(FLASH_MODES[mode])

    def is_metering_mode_supported(self, mode: str) -> bool:
        if mode not in METERING_MODES:
            raise InvalidParamError(mode, METERING_MODES)
        return self.item.isMeteringModeSupported(METERING_MODES[mode])


if __name__ == "__main__":
    cam = multimedia.Camera()
    focus = cam.get_focus()
