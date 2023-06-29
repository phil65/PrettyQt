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
- allows strings which represent an existing path. Can be set to either accept files, folders or both.

`PythonCodeValidator`
- allows a string which can be parsed by ast.parse

`QssValidator`
- allows a string which can be parsed as CSS.

`RegexPatternValidator`
- allows a string which can be parsed as a regular expression.

`IntListValidator`
- allows a comma separated list of integers

`FloatListValidator`
- allows a comma separated list of floats

`ScientificIntegerValidator`
 - for integers in scientific annotation. also allows SI unit prefix like 'M', 'n' etc.

`ScientificFloatValidator`
 - for floats in scientific annotation. also allows SI unit prefix like 'M', 'n' etc.

`TextLengthValidator`
- allows limiting textlength to a given minimum / maximim

`WhitelistValidator`
- whitelist specific strings

`FunctionValidator`
- validate string based on a Callable (Signature: Callable[[str], bool])


Apart from LineEdits, ComboBoxes and SpinBoxes, PlainTextEdits also gained the ability to take a validator.

The set_validator method also gained a "strict" keyword argument, which wraps the passed
validator into a NotStrictValidator, effectively removing the "Invalid" state. That way
there never is a situation where the user input is ignored, which might be preferred in a lot of situations.

The acceptance of "" may also be overriden explicitely by setting the "allow_empty" keyword argument.

Validators which inherit from gui.Validator also can be combined.

Example:
    and_val = BlackListValidator(["Blacklisted word"]) & AlphanumericValidator()  # returns an AndValidator
    or_val = AlphanumericValidator() | RegularExpressionValidator("some_regex") # returns an OrValidator

Validators can also be set by an id. Since everything is typed with Literals, the possible ids should be shown by your IDE.

    lineedit.set_validator("float")

