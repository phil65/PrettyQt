from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


FlagStr = Literal["hidden_from_help", "short_option_style"]

FLAGS: bidict[FlagStr, core.QCommandLineOption.Flag] = bidict(
    hidden_from_help=core.QCommandLineOption.Flag.HiddenFromHelp,
    short_option_style=core.QCommandLineOption.Flag.ShortOptionStyle,
)


class CommandLineOption(core.QCommandLineOption):
    """Defines a possible command-line option."""
