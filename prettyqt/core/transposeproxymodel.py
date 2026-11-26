from prettyqt import core


class TransposeProxyModel(core.AbstractProxyModelMixin, core.QTransposeProxyModel):
    """This proxy transposes the source model."""

    ID = "transpose"
