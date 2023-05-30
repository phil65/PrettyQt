from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtDesigner


class DesignerFormEditorInterface(
    core.ObjectMixin, QtDesigner.QDesignerFormEditorInterface
):
    pass


if __name__ == "__main__":
    interface = DesignerFormEditorInterface()
