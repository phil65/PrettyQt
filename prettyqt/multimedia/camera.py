from typing import List, Literal

from qtpy import QtMultimedia

from prettyqt import multimedia
from prettyqt.utils import InvalidParamError, bidict, mappers


CAPTURE_MODES = mappers.FlagMap(
    QtMultimedia.QCamera.CaptureModes,
    viewfinder=QtMultimedia.QCamera.CaptureViewfinder,
    still_image=QtMultimedia.QCamera.CaptureStillImage,
    video=QtMultimedia.QCamera.CaptureVideo,
)

CaptureModeStr = Literal["viewfinder", "still_image", "video"]

ERROR = bidict(
    none=QtMultimedia.QCamera.NoError,
    camera=QtMultimedia.QCamera.CameraError,
    invalid_request=QtMultimedia.QCamera.InvalidRequestError,
    service_missing=QtMultimedia.QCamera.ServiceMissingError,
    not_supported_feature=QtMultimedia.QCamera.NotSupportedFeatureError,
)

ErrorStr = Literal[
    "none", "camera", "invalid_request", "service_missing", "not_supported_feature"
]

LOCK_CHANGE_REASONS = bidict(
    user_request=QtMultimedia.QCamera.UserRequest,
    lock_acquired=QtMultimedia.QCamera.LockAcquired,
    lock_failed=QtMultimedia.QCamera.LockFailed,
    lock_lost=QtMultimedia.QCamera.LockLost,
    lock_temporary_lost=QtMultimedia.QCamera.LockTemporaryLost,
)

LockChangeReasonStr = Literal[
    "user_request",
    "lock_acquired",
    "lock_failed",
    "lock_lost",
    "lock_temporary_lost",
]

LOCK_STATUS = bidict(
    unlocked=QtMultimedia.QCamera.Unlocked,
    searching=QtMultimedia.QCamera.Searching,
    locked=QtMultimedia.QCamera.Locked,
)

LockStatusStr = Literal["unlocked", "searching", "locked"]

LOCK_TYPES = bidict(
    none=QtMultimedia.QCamera.NoLock,
    exposure=QtMultimedia.QCamera.LockExposure,
    white_balance=QtMultimedia.QCamera.LockWhiteBalance,
    focus=QtMultimedia.QCamera.LockFocus,
)

LockTypeStr = Literal["none", "exposure", "white_balance", "focus"]

POSITIONS = bidict(
    unspecified=QtMultimedia.QCamera.UnspecifiedPosition,
    back_face=QtMultimedia.QCamera.BackFace,
    front_face=QtMultimedia.QCamera.FrontFace,
)

PositionStr = Literal["unspecified", "back_face", "front_face"]

STATES = bidict(
    unloaded=QtMultimedia.QCamera.UnloadedState,
    loaded=QtMultimedia.QCamera.LoadedState,
    active=QtMultimedia.QCamera.ActiveState,
)

StateStr = Literal["unloaded", "loaded", "active"]

STATUS = bidict(
    active=QtMultimedia.QCamera.ActiveStatus,
    starting=QtMultimedia.QCamera.StartingStatus,
    stopping=QtMultimedia.QCamera.StoppingStatus,
    standby=QtMultimedia.QCamera.StandbyStatus,
    loaded=QtMultimedia.QCamera.LoadedStatus,
    loading=QtMultimedia.QCamera.LoadingStatus,
    unloading=QtMultimedia.QCamera.UnloadingStatus,
    unloaded=QtMultimedia.QCamera.UnloadedStatus,
    unavailable=QtMultimedia.QCamera.UnavailableStatus,
)

StatusStr = Literal[
    "active",
    "starting",
    "stopping",
    "standby",
    "loaded",
    "loading",
    "unloading",
    "unloaded",
    "unavailable",
]

QtMultimedia.QCamera.__bases__ = (multimedia.MediaObject,)


class Camera(QtMultimedia.QCamera):
    def get_state(self) -> StateStr:
        """Return current state.

        Returns:
            state
        """
        return STATES.inverse[self.state()]

    def get_status(self) -> StatusStr:
        """Return current status.

        Returns:
            status
        """
        return STATUS.inverse[self.status()]

    def get_lock_status(self) -> LockStatusStr:
        """Return current lock status.

        Returns:
            lock status
        """
        return LOCK_STATUS.inverse[self.lockStatus()]

    def get_error(self) -> ErrorStr:
        """Return current error state.

        Returns:
            error state
        """
        return ERROR.inverse[self.error()]

    def set_capture_mode(self, position: CaptureModeStr):
        """Set the capture mode.

        Args:
            position: capture mode

        Raises:
            InvalidParamError: capture mode does not exist
        """
        if position not in CAPTURE_MODES:
            raise InvalidParamError(position, CAPTURE_MODES)
        self.setCaptureMode(CAPTURE_MODES[position])

    def get_capture_mode(self) -> CaptureModeStr:
        """Return current capture mode.

        Returns:
            capture mode
        """
        return CAPTURE_MODES.inverse[self.captureMode()]

    def get_supported_locks(self) -> List[LockTypeStr]:
        return [k for k, v in LOCK_TYPES.items() if v & self.supportedLocks()]

    def get_requested_locks(self) -> List[LockTypeStr]:
        return [k for k, v in LOCK_TYPES.items() if v & self.requestedLocks()]

    def get_focus(self) -> multimedia.CameraFocus:
        return multimedia.CameraFocus(self.focus())

    def get_exposure(self) -> multimedia.CameraExposure:
        return multimedia.CameraExposure(self.exposure())

    def get_image_processing(self) -> multimedia.CameraImageProcessing:
        return multimedia.CameraImageProcessing(self.imageProcessing())
