from __future__ import annotations

from prettyqt import widgets


class CommonStyleMixin(widgets.StyleMixin):
    pass


class CommonStyle(CommonStyleMixin, widgets.QCommonStyle):
    """Encapsulates the common Look and Feel of a GUI."""


if __name__ == "__main__":
    style = CommonStyle()
