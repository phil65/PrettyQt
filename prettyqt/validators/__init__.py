"""PrettyQt Validators.

PrettyQt ships a large number of predefined validators.

Apart from LineEdits, ComboBoxes and SpinBoxes, PlainTextEdits also gained the ability
to take a validator.

The set_validator method also gained a "strict" keyword argument, which wraps the passed
validator into a NotStrictValidator, effectively removing the "Invalid" state. That way
there never is a situation where the user input is ignored, which might be preferred in a
lot of situations.

The acceptance of "" may also be overriden explicitely by setting the "allow_empty"
keyword argument.

Validators can also be combined. The resulting CompositeValidator checks if all
containing validators accept the input.


Example:
```py
val_1 = BlackListValidator(["Blacklisted word"])
val_2 = AlphanumericValidator()
and_validator = val_1 & val_2  # returns an AndValidator

val_1 = AlphanumericValidator()
val_2 = RegularExpressionValidator("some_regex")
or_val = val_1 | val_2 # returns an OrValidator
```
Validators can also be set by an id. Since everything is typed with Literals,
the possible ids should be shown by your IDE.
```py
lineedit.set_validator("float")
```

"""

from __future__ import annotations

from .alphanumericvalidator import AlphaNumericValidator
from .blacklistvalidator import BlacklistValidator, NotEmptyValidator, NotZeroValidator
from .colorvalidator import ColorValidator
from .compositevalidator import AndValidator, OrValidator
from .functionvalidator import FunctionValidator
from .hexvalidator import HexValidator
from .integervalidator import IntegerValidator
from .jsonvalidator import JsonValidator
from .monotoniclistvalidator import MonotonicListValidator
from .notstrictvalidator import NotStrictValidator
from .pathvalidator import PathValidator
from .pythoncodevalidator import PythonCodeValidator
from .qssvalidator import QssValidator
from .regexpatternvalidator import RegexPatternValidator
from .regexvalidators import FloatListValidator, IntListValidator
from .scientificvalidators import ScientificFloatValidator, ScientificIntegerValidator
from .textlengthvalidator import TextLengthValidator
from .whitelistvalidator import EmptyValidator, WhitelistValidator


__all__ = [
    "AlphaNumericValidator",
    "AndValidator",
    "BlacklistValidator",
    "ColorValidator",
    "EmptyValidator",
    "FloatListValidator",
    "FunctionValidator",
    "HexValidator",
    "IntListValidator",
    "IntegerValidator",
    "JsonValidator",
    "MonotonicListValidator",
    "NotEmptyValidator",
    "NotStrictValidator",
    "NotZeroValidator",
    "OrValidator",
    "PathValidator",
    "PythonCodeValidator",
    "QssValidator",
    "RegexPatternValidator",
    "ScientificFloatValidator",
    "ScientificIntegerValidator",
    "TextLengthValidator",
    "WhitelistValidator",
]
