from __future__ import annotations

import re

from prettyqt import gui


class BaseScientificValidator(gui.Validator):
    re_pattern: re.Pattern
    group_map: dict[str, int]

    def get_group_dict(self, string: str):
        """Match the input string with the regex of this validator.

        The match groups will be put into a dict with strings  as keys describing
        the role of the specific group (i.e. mantissa, exponent, si-prefix etc.)

        Arguments:
            string: input string to be matched

        Returns:
            dictionary containing groups as items and strings as keys
        """
        match = self.re_pattern.search(string)
        if not match:
            return False
        groups = match.groups()
        return {k: groups[self.group_map[k]] for k in self.group_map}

    def fixup(self, text):
        return (
            match.groups()[0].strip() if (match := self.re_pattern.search(text)) else ""
        )


class ScientificIntegerValidator(BaseScientificValidator):
    """This is a validator for int values represented as strings in scientific notation.

    Using engineering notation only positive exponents are allowed
    (i.e. "1e9", "2E+8", "14e+3" etc.)
    Also supports non-fractional SI unit prefix like 'M', 'k' etc.
    """

    ID = "scientific_integer"

    re_pattern = re.compile(
        r"(([+-]?\d+)([eE]\+?\d+)?\s?([YZEPTGMk])?\s*)", flags=re.UNICODE
    )
    group_map = {"match": 0, "mantissa": 1, "exponent": 2, "si": 3}

    def validate(self, string, position):
        if not string.strip() or string.strip() in list("YZEPTGMk"):
            return self.State.Intermediate, string, position

        if not (group_dict := self.get_group_dict(string)):
            return self.invalid_value(), "", position
        if group_dict["match"] == string:
            return self.State.Acceptable, string, position

        position = min(position, len(string))
        if string[position - 1] in "eE-+":
            return self.State.Intermediate, string, position

        return self.invalid_value(), group_dict["match"], position


class ScientificFloatValidator(BaseScientificValidator):
    """This is a validator for float values represented as strings in scientific notation.

    (i.e. "1.35e-9", ".24E+8", "14e3" etc.)
    Also supports SI unit prefix like 'M', 'n' etc.
    """

    ID = "scientific_float"
    re_pattern = re.compile(
        r"(\s*([+-]?)(\d+\.\d+|\.\d+|\d+\.?)([eE][+-]?\d+)?\s?([YZEPTGMkmµunpfazy]?)\s*)",
        flags=re.UNICODE,
    )
    group_map = {"match": 0, "sign": 1, "mantissa": 2, "exponent": 3, "si": 4}

    def validate(self, string, position):
        if (
            string.strip() in "+.-."
            or string.strip() in list("YZEPTGMkmµunpfazy")
            or re.match(r"[+-]?(in$|i$)", string, re.IGNORECASE)
        ):
            return self.State.Intermediate, string, position

        # Accept input of [+-]inf. Not case sensitive.
        if re.match(r"[+-]?\binf$", string, re.IGNORECASE):
            return self.State.Acceptable, string.lower(), position

        if not (group_dict := self.get_group_dict(string)):
            return (
                (self.State.Intermediate, string, position)
                if string[position - 1] in "eE-+." and "i" not in string.lower()
                else (self.invalid_value(), "", position)
            )
        if group_dict["match"] == string:
            return self.State.Acceptable, string, position
        if string.count(".") > 1:
            return self.invalid_value(), group_dict["match"], position
        position = min(position, len(string))
        if string[position - 1] in "eE-+" and "i" not in string.lower():
            return self.State.Intermediate, string, position
        return self.invalid_value(), group_dict["match"], position
