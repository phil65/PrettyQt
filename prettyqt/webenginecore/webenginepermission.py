from typing import Literal

from prettyqt import core
from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import bidict, get_repr


mod = QtWebEngineCore.QWebEnginePermission

PermissionTypeStr = Literal[
    "unsupported",
    "media_audio_capture",
    "media_video_capture",
    "media_audiovideo_capture",
    "desktop_video_capture",
    "desktop_audiovideo_capture",
    "mouse_lock",
    "notifications",
    "geolocation",
    "clipboard_read_write",
    "local_fonts_access",
]

PERMISSION_TYPE: bidict[PermissionTypeStr, mod.PermissionType] = bidict(
    unsupported=mod.PermissionType.Unsupported,
    media_audio_capture=mod.PermissionType.MediaAudioCapture,
    media_video_capture=mod.PermissionType.MediaVideoCapture,
    media_audiovideo_capture=mod.PermissionType.MediaAudioVideoCapture,
    desktop_video_capture=mod.PermissionType.DesktopVideoCapture,
    desktop_audiovideo_capture=mod.PermissionType.DesktopAudioVideoCapture,
    mouse_lock=mod.PermissionType.MouseLock,
    notifications=mod.PermissionType.Notifications,
    geolocation=mod.PermissionType.Geolocation,
    clipboard_read_write=mod.PermissionType.ClipboardReadWrite,
    local_fonts_access=mod.PermissionType.LocalFontsAccess,
)

StateStr = Literal["invalid", "ask", "granted", "denied"]

STATE: bidict[StateStr, mod.State] = bidict(
    invalid=mod.State.Invalid,
    ask=mod.State.Ask,
    granted=mod.State.Granted,
    denied=mod.State.Denied,
)


class WebEnginePermission(QtWebEngineCore.QWebEnginePermission):
    """Represents a permission request or stored permission for a web origin."""

    def __repr__(self):
        return get_repr(
            self,
            self.get_origin(),
            self.get_permission_type(),
            self.get_state(),
        )

    def __bool__(self):
        return self.isValid()

    def get_origin(self) -> core.Url:
        """Return the origin URL associated with this permission."""
        return core.Url(self.origin())

    def get_permission_type(self) -> PermissionTypeStr:
        """Return the permission type."""
        return PERMISSION_TYPE.inverse[self.permissionType()]

    def get_state(self) -> StateStr:
        """Return the current permission state."""
        return STATE.inverse[self.state()]

    @classmethod
    def is_persistent(
        cls, permission_type: PermissionTypeStr | mod.PermissionType
    ) -> bool:
        """Return whether the given permission type is persistent."""
        return cls.isPersistent(PERMISSION_TYPE.get_enum_value(permission_type))


if __name__ == "__main__":
    perm = WebEnginePermission()
    print(repr(perm))
