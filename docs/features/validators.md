# Validators

PrettyQt includes a range of pre-defined validators.

The following validators are included:

`AlphanumericValidator`

`BlacklistValidator`

`ColorValidator`

`CompositeValidator`

`HexValidator`

`IntegerValidator`

`JsonValidator`

`MonotonicListValidator`

`NotStrictValidator`

`PathValidator`

`PythonCodeValidator`

`QssValidator`

`RegexPatternValidator`

`IntListValidator`

`FloatListValidator`

`ScientificIntegerValidator`

`ScientificFloatValidator`

`TextLengthValidator`

`WhitelistValidator`


Apart from LineEdits, PlainTextEdits also gained the ability to take a validator.

The set_validator method also gained a "strict" keyword argument, which wraps the passed
validator into a NotStrictValidator, effectively removing the "Invalid" state. That way
there never is a situation where the user input is ignored, which might be preferred in a lot of situations.

Validators which inherit from gui.Validator also can be combined.

Example:
    and_val = BlackListValidator(["Blacklisted word"]) & AlphanumericValidator()  # returns an AndValidator
    or_val = AlphanumericValidator() | RegularExpressionValidator("some_regex") # returns an OrValidator

Validators can also be set by an id. Since everything is typed with Literals, the possible ids should be shown by your IDE.

    lineedit.set_validator("float")

