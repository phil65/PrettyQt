from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtDesigner


class PyDesignerTaskMenuExtension(
    core.ObjectMixin, QtDesigner.QPyDesignerTaskMenuExtension
):
    def preferredEditAction(self):
        return NotImplemented

    def taskActions(self):
        return NotImplemented


if __name__ == "__main__":
    obj = core.Object()
    ext = PyDesignerTaskMenuExtension(obj)
    new = dir(PyDesignerTaskMenuExtension(obj))
    bie = dir(core.Object())
    c = [x for x in new if x not in bie]
