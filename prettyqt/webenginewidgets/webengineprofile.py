# -*- coding: utf-8 -*-

# from qtpy import QtWebEngineWidgets

try:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
except ImportError:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


HTTP_CACHE_TYPES = bidict(
    none=QtWebEngineWidgets.QWebEngineProfile.NoCache,
    disk=QtWebEngineWidgets.QWebEngineProfile.DiskHttpCache,
    memory=QtWebEngineWidgets.QWebEngineProfile.MemoryHttpCache,
)

PERSISTENT_COOKIE_POLICIES = bidict(
    none=QtWebEngineWidgets.QWebEngineProfile.NoPersistentCookies,
    allow=QtWebEngineWidgets.QWebEngineProfile.AllowPersistentCookies,
    force=QtWebEngineWidgets.QWebEngineProfile.ForcePersistentCookies,
)

QtWebEngineWidgets.QWebEngineProfile.__bases__ = (core.Object,)


class WebEngineProfile(QtWebEngineWidgets.QWebEngineProfile):
    def set_persistent_cookie_policy(self, policy: str):
        """Set the persistent cookie policy.

        Allowed values are "none", "allow", "force"

        Args:
            policy: persistent cookie policy

        Raises:
            InvalidParamError: Policy does not exist
        """
        if policy not in PERSISTENT_COOKIE_POLICIES:
            raise InvalidParamError(policy, PERSISTENT_COOKIE_POLICIES)
        self.setPersistentCookiesPolicy(PERSISTENT_COOKIE_POLICIES[policy])

    def get_persistent_cookie_policy(self) -> str:
        """Return current persistent cookie policy.

        Possible values are "none", "allow", "force"

        Returns:
            Save page format
        """
        return PERSISTENT_COOKIE_POLICIES.inv[self.persistentCookiesPolicy()]

    def set_http_cache_type(self, typ: str):
        """Set the http cache type.

        Allowed values are "none", "disk", "memory"

        Args:
            type: http cache type

        Raises:
            InvalidParamError: Cache type does not exist
        """
        if typ not in HTTP_CACHE_TYPES:
            raise InvalidParamError(typ, HTTP_CACHE_TYPES)
        self.setHttpCacheType(HTTP_CACHE_TYPES[typ])

    def get_http_cache_type(self) -> str:
        """Return current http cache type.

        Possible values are "none", "disk", "memory"

        Returns:
            Http cache type
        """
        return HTTP_CACHE_TYPES.inv[self.httpCacheType()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    item = WebEngineProfile()
    app.main_loop()
