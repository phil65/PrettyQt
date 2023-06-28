from __future__ import annotations

from prettyqt import widgets


class StyleOptionComplexMixin(widgets.StyleOptionMixin):
    pass


class StyleOptionComplex(StyleOptionComplexMixin, widgets.QStyleOptionComplex):
    pass
