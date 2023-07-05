PrettyQt includes a range of pre-defined validators.

The following validators are included:


| Validator                | Description                                |
|--------------------------|--------------------------------------------|
|`AlphanumericValidator`
|`BlacklistValidator`
|`ColorValidator`
|`CompositeValidator`
|`HexValidator`
|`IntegerValidator`
|`JsonValidator`
|`MonotonicListValidator`
|`NotStrictValidator`
|`PathValidator` |allows strings which represent an existing path. Can be set to either accept files, folders or both
|`PythonCodeValidator`| Allows a string which can be parsed by ast.parse
|`QssValidator`| Allows a string which can be parsed as CSS
|`RegexPatternValidator`| Allows a string which can be parsed as a regular expression
|`IntListValidator`| Allows a comma separated list of integers
|`FloatListValidator`| Allows a comma separated list of floats
|`ScientificIntegerValidator`|  For integers in scientific annotation. also allows SI unit prefix like 'M', 'n' etc.
|`ScientificFloatValidator`|  For floats in scientific annotation. also allows SI unit prefix like 'M', 'n' etc.
|`TextLengthValidator`| Allows limiting textlength to a given minimum / maximum
|`WhitelistValidator`| Whitelist specific strings
|`FunctionValidator`| Validate string based on a Callable (Signature: Callable[[str], bool])


Apart from LineEdits, ComboBoxes and SpinBoxes, PlainTextEdits also gained the ability to take a validator.

The set_validator method also gained a "strict" keyword argument, which wraps the passed
validator into a NotStrictValidator, effectively removing the "Invalid" state. That way
there never is a situation where the user input is ignored, which might be preferred in a lot of situations.

The acceptance of "" may also be overriden explicitely by setting the "allow_empty" keyword argument.

Validators which inherit from gui.Validator also can be combined.

Example:
```py
val_1 = BlackListValidator(["Blacklisted word"])
val_2 = AlphanumericValidator()
and_validator = val_1 & val_2  # returns an AndValidator

val_1 = AlphanumericValidator()
val_2 = RegularExpressionValidator("some_regex")
or_val = val_1 | val_2 # returns an OrValidator
```
Validators can also be set by an id. Since everything is typed with Literals, the possible ids should be shown by your IDE.
```py
lineedit.set_validator("float")
```
