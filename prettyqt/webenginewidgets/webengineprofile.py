# from qtpy import QtWebEngineWidgets

from typing import Literal

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core, webenginewidgets
from prettyqt.utils import InvalidParamError, bidict


HTTP_CACHE_TYPE = bidict(
    none=QtWebEngineWidgets.QWebEngineProfile.NoCache,
    disk=QtWebEngineWidgets.QWebEngineProfile.DiskHttpCache,
    memory=QtWebEngineWidgets.QWebEngineProfile.MemoryHttpCache,
)

HttpCacheTypeStr = Literal["none", "disk", "memory"]

PERSISTENT_COOKIE_POLICY = bidict(
    none=QtWebEngineWidgets.QWebEngineProfile.NoPersistentCookies,
    allow=QtWebEngineWidgets.QWebEngineProfile.AllowPersistentCookies,
    force=QtWebEngineWidgets.QWebEngineProfile.ForcePersistentCookies,
)

PersistentCookiePolicyStr = Literal["none", "allow", "force"]

QtWebEngineWidgets.QWebEngineProfile.__bases__ = (core.Object,)


class WebEngineProfile(QtWebEngineWidgets.QWebEngineProfile):
    def set_persistent_cookie_policy(self, policy: PersistentCookiePolicyStr):
        """Set the persistent cookie policy.

        Args:
            policy: persistent cookie policy

        Raises:
            InvalidParamError: Policy does not exist
        """
        if policy not in PERSISTENT_COOKIE_POLICY:
            raise InvalidParamError(policy, PERSISTENT_COOKIE_POLICY)
        self.setPersistentCookiesPolicy(PERSISTENT_COOKIE_POLICY[policy])

    def get_persistent_cookie_policy(self) -> PersistentCookiePolicyStr:
        """Return current persistent cookie policy.

        Returns:
            Persistent cookie policy
        """
        return PERSISTENT_COOKIE_POLICY.inverse[self.persistentCookiesPolicy()]

    def set_http_cache_type(self, typ: HttpCacheTypeStr):
        """Set the http cache type.

        Args:
            typ: http cache type

        Raises:
            InvalidParamError: Cache type does not exist
        """
        if typ not in HTTP_CACHE_TYPE:
            raise InvalidParamError(typ, HTTP_CACHE_TYPE)
        self.setHttpCacheType(HTTP_CACHE_TYPE[typ])

    def get_http_cache_type(self) -> HttpCacheTypeStr:
        """Return current http cache type.

        Returns:
            Http cache type
        """
        return HTTP_CACHE_TYPE.inverse[self.httpCacheType()]

    def get_scripts(self) -> webenginewidgets.WebEngineScriptCollection:
        return webenginewidgets.WebEngineScriptCollection(self.scripts())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    item = WebEngineProfile()
    app.main_loop()
