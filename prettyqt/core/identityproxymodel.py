from __future__ import annotations

from prettyqt import core


class IdentityProxyModel(core.AbstractProxyModelMixin, core.QIdentityProxyModel):
    """Proxies its source model unmodified."""

    ID = "identity"
