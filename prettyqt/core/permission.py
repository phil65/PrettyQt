from prettyqt import constants, core
from prettyqt.utils import get_repr


class Permission(core.QPermission):
    """Opaque wrapper of a typed permission."""

    def __repr__(self):
        return get_repr(self, self.get_status())

    def get_status(self) -> constants.PermissionStatusStr:
        """Return current permission status.

        Returns:
            permission status
        """
        return constants.PERMISSION_STATUS.inverse[self.status()]

    def get_type(self) -> core.MetaType:
        """Return the meta-type of the wrapped permission.

        Returns:
            permission meta-type
        """
        return core.MetaType(self.type().id())
