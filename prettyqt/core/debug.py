# from prettyqt.qt import QtCore

# from prettyqt.utils import bidict, InvalidParamError

from __future__ import annotations


# VERBOSITY_LEVEL = bidict(
#     minimum=QtCore.QDebug.MinimumVerbosity,
#     default=QtCore.QDebug.DefaultVerbosity,
#     maximum=QtCore.QDebug.MaximumVerbosity,
# )

# class Debug(QtCore.QDebug):
#     def set_verbosity(self, verbosity: str):
#         """Set the debug verbosity.

#         Valid values are "minimum", "default", "maximum"

#         Args:
#             verbosity: debug verbosity

#         Raises:
#             InvalidParamError: invalid debug verbosity
#         """
#         if verbosity not in VERBOSITY_LEVEL:
#             raise InvalidParamError(verbosity, VERBOSITY_LEVEL)
#         self.setVerbosity(VERBOSITY_LEVEL[verbosity])

#     def get_verbosity(self) -> str:
#         """Get current debug verbosity.

#         Possible values are "minimum", "default", "maximum"

#         Returns:
#             current debug verbosity
#         """
#         return VERBOSITY_LEVEL.inverse[self.verbosity()]


# if __name__ == "__main__":
#     matcher = Debug("Test")
#     print(repr(matcher))
