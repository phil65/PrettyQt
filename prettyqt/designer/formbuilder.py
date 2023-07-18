from __future__ import annotations

from prettyqt import designer


class FormBuilder(
    designer.abstractformbuilder.AbstractFormBuilderMixin, designer.QFormBuilder
):
    """Used to dynamically construct user interfaces from UI files at run-time."""


if __name__ == "__main__":
    builder = FormBuilder()
