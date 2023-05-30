from __future__ import annotations

from prettyqt import designer
from prettyqt.qt import QtDesigner


class FormBuilder(
    designer.abstractformbuilder.AbstractFormBuilderMixin, QtDesigner.QFormBuilder
):
    pass


if __name__ == "__main__":
    builder = FormBuilder()
