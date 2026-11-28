from prettyqt import core
from prettyqt.qt import QtCore


class StringEncoder(core.StringConverterMixin, QtCore.QStringEncoder):
    """State-based encoder for text."""

    def __init__(
        self,
        encoding: core.stringconverter.EncodingStr
        | QtCore.QStringConverter.Encoding
        | str
        | None = None,
        flags: core.stringconverter.FlagStr | QtCore.QStringConverter.Flag | None = None,
    ):
        if encoding is None:
            super().__init__()
            return
        enc: QtCore.QStringConverter.Encoding | str
        if isinstance(encoding, str) and encoding in core.stringconverter.ENCODING:
            enc = core.stringconverter.ENCODING[encoding]  # type: ignore[index]
        else:
            enc = encoding
        if flags is None:
            super().__init__(enc)
        else:
            flag_val = core.stringconverter.FLAG.get_enum_value(flags)
            super().__init__(enc, flag_val)
