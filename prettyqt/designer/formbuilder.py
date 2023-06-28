from __future__ import annotations

from prettyqt import designer


class FormBuilder(
    designer.abstractformbuilder.AbstractFormBuilderMixin, designer.QFormBuilder
):
    pass


if __name__ == "__main__":
    builder = FormBuilder()
