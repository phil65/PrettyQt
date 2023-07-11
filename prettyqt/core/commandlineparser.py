from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


mod = core.QCommandLineParser
op = mod.OptionsAfterPositionalArgumentsMode

OptionsAfterPosArgStr = Literal["options", "positional_arguments"]

OPTIONS_AFTER_POS_ARG: bidict[OptionsAfterPosArgStr, op] = bidict(
    options=op.ParseAsOptions,
    positional_arguments=op.ParseAsPositionalArguments,
)

SingleDashWordStr = Literal["compacted_short", "long"]

SINGLE_DASH_WORD: bidict[SingleDashWordStr, mod.SingleDashWordOptionMode] = bidict(
    compacted_short=mod.SingleDashWordOptionMode.ParseAsCompactedShortOptions,
    long=mod.SingleDashWordOptionMode.ParseAsLongOptions,
)


class CommandLineParser(core.QCommandLineParser):
    """Means for handling the command line options."""

    def set_single_dash_word_option_mode(self, mode: SingleDashWordStr):
        """Set the single dash word option mode.

        Args:
            mode: single dash word option mode
        """
        self.setSingleDashWordOptionMode(SINGLE_DASH_WORD.get_enum_value(mode))

    def set_options_after_positional_arguments_mode(
        self, mode: SingleDashWordStr | mod.SingleDashWordOptionMode
    ):
        """Set the options after positional arguments mode.

        Args:
            mode: options after positional arguments mode
        """
        val = OPTIONS_AFTER_POS_ARG.get_enum_value(mode)
        self.setOptionsAfterPositionalArgumentsMode(val)

    def add_option(
        self,
        name: str,
        description: str | None = None,
        value_name: str | None = None,
        default_value: str | None = None,
    ) -> core.CommandLineOption:
        if description is None:
            description = ""
        if value_name is None:
            value_name = ""
        if default_value is None:
            default_value = ""
        option = core.CommandLineOption(name, description, value_name, default_value)
        self.addOption(option)
        return option
