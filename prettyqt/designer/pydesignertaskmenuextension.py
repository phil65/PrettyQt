from prettyqt import core
from prettyqt.qt import QtDesigner


class PyDesignerTaskMenuExtension(
    core.ObjectMixin, QtDesigner.QPyDesignerTaskMenuExtension
):
    def preferredEditAction(self):
        raise NotImplementedError

    def taskActions(self):
        raise NotImplementedError


if __name__ == "__main__":
    obj = core.Object()
    ext = PyDesignerTaskMenuExtension(obj)
    new = dir(PyDesignerTaskMenuExtension(obj))
    bie = dir(core.Object())
    c = [x for x in new if x not in bie]
