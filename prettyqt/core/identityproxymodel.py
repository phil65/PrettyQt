from __future__ import annotations

from prettyqt import core


class IdentityProxyModel(core.AbstractProxyModelMixin, core.QIdentityProxyModel):
    ID = "identity"
