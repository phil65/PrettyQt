from __future__ import annotations

from prettyqt import widgets


class ProxyStyle(widgets.CommonStyleMixin, widgets.QProxyStyle):
    """Convenience class that simplifies dynamically overriding QStyle elements."""


if __name__ == "__main__":
    style = ProxyStyle()
