from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtWidgets


class GraphicsEffectMixin(core.ObjectMixin):
    pass

class GraphicsEffect(GraphicsEffectMixin, QtWidgets.QGraphicsEffect):
    pass
