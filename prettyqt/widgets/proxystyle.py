from __future__ import annotations

from prettyqt import widgets


class ProxyStyle(widgets.CommonStyleMixin, widgets.QProxyStyle):
    pass


if __name__ == "__main__":
    style = ProxyStyle()
