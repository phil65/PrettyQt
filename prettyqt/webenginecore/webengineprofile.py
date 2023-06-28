from __future__ import annotations

from typing import Literal

from prettyqt import core, webenginecore
from prettyqt.utils import bidict


mod = webenginecore.QWebEngineProfile

HttpCacheTypeStr = Literal["none", "disk", "memory"]

HTTP_CACHE_TYPE: bidict[HttpCacheTypeStr, mod.HttpCacheType] = bidict(
    none=mod.HttpCacheType.NoCache,
    disk=mod.HttpCacheType.DiskHttpCache,
    memory=mod.HttpCacheType.MemoryHttpCache,
)

PersistentCookiePolicyStr = Literal["none", "allow", "force"]

PERSISTENT_COOKIE_POLICY: bidict[
    PersistentCookiePolicyStr, mod.PersistentCookiesPolicy
] = bidict(
    none=mod.PersistentCookiesPolicy.NoPersistentCookies,
    allow=mod.PersistentCookiesPolicy.AllowPersistentCookies,
    force=mod.PersistentCookiesPolicy.ForcePersistentCookies,
)


class WebEngineProfile(core.ObjectMixin, webenginecore.QWebEngineProfile):
    def set_persistent_cookie_policy(
        self, policy: PersistentCookiePolicyStr | mod.PersistentCookiesPolicy
    ):
        """Set the persistent cookie policy.

        Args:
            policy: persistent cookie policy
        """
        self.setPersistentCookiesPolicy(PERSISTENT_COOKIE_POLICY.get_enum_value(policy))

    def get_persistent_cookie_policy(self) -> PersistentCookiePolicyStr:
        """Return current persistent cookie policy.

        Returns:
            Persistent cookie policy
        """
        return PERSISTENT_COOKIE_POLICY.inverse[self.persistentCookiesPolicy()]

    def set_http_cache_type(self, typ: HttpCacheTypeStr | mod.PersistentCookiesPolicy):
        """Set the http cache type.

        Args:
            typ: http cache type
        """
        self.setHttpCacheType(HTTP_CACHE_TYPE.get_enum_value(typ))

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
    app.exec()
