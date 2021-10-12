# from prettyqt.qt import QtWebEngineCore

from __future__ import annotations

from typing import Literal

from prettyqt import core, webenginecore
from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import InvalidParamError, bidict


mod = QtWebEngineCore.QWebEngineProfile

HTTP_CACHE_TYPE = bidict(
    none=mod.HttpCacheType.NoCache,
    disk=mod.HttpCacheType.DiskHttpCache,
    memory=mod.HttpCacheType.MemoryHttpCache,
)

HttpCacheTypeStr = Literal["none", "disk", "memory"]

PERSISTENT_COOKIE_POLICY = bidict(
    none=mod.PersistentCookiesPolicy.NoPersistentCookies,
    allow=mod.PersistentCookiesPolicy.AllowPersistentCookies,
    force=mod.PersistentCookiesPolicy.ForcePersistentCookies,
)

PersistentCookiePolicyStr = Literal["none", "allow", "force"]

QtWebEngineCore.QWebEngineProfile.__bases__ = (core.Object,)


class WebEngineProfile(QtWebEngineCore.QWebEngineProfile):
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

    def get_scripts(self) -> webenginecore.WebEngineScriptCollection:
        return webenginecore.WebEngineScriptCollection(self.scripts())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    item = WebEngineProfile()
    app.main_loop()
