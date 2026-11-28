"""Tests for `prettyqt` package."""

import inspect
import pathlib
import pickle

from prettyqt import validators


clsmembers = inspect.getmembers(validators, inspect.isclass)


def pickle_roundtrip(something):
    path = pathlib.Path("data.pkl")
    with path.open("wb") as jar:
        pickle.dump(something, jar)
    with path.open("rb") as jar:
        return pickle.load(jar)


# @pytest.mark.parametrize("name, cls", clsmembers)
# def test_pickle(name, cls):
#     vale = cls()
#     with open("data.pkl", "wb") as jar:
#         pickle.dump(vale, jar)
#     with open("data.pkl", "rb") as jar:
#         vale = pickle.load(jar)


def test_pathvalidator():
    val = validators.PathValidator()
    val = pickle_roundtrip(val)
    assert val.is_valid_value(str(pathlib.Path.cwd()))
    assert not val.is_valid_value("abs")
    repr(val)
    assert val == validators.PathValidator()
    assert val != validators.NotZeroValidator()


def test_notzerovalidator():
    val = validators.NotZeroValidator()
    assert val.is_valid_value("1")
    assert not val.is_valid_value("0")
    repr(val)
    assert val != validators.PathValidator()
    assert val == validators.NotZeroValidator()


def test_notemptyvalidator():
    val = validators.NotEmptyValidator()
    assert val.is_valid_value("1")
    assert not val.is_valid_value("")
    repr(val)
    assert val != validators.PathValidator()
    assert val == validators.NotEmptyValidator()


def test_andvalidator():
    val1 = validators.NotEmptyValidator()
    val2 = validators.NotZeroValidator()
    composite = validators.AndValidator([val1, val2])
    assert composite != validators.PathValidator()
    assert composite == validators.AndValidator([val1, val2])
    composite = pickle_roundtrip(composite)
    assert composite.is_valid_value("1")
    assert not composite.is_valid_value("")
    assert not composite.is_valid_value("0")
    val1 & val2
    for _child in composite:
        pass
    assert val1 in composite
    assert val1 == composite[0]
    composite[1] = validators.NotZeroValidator()
    assert len(composite) == 2  # noqa: PLR2004
    del composite[1]
    repr(composite)


def test_intlistvalidator():
    val = validators.IntListValidator(allow_single=True)
    assert val.is_valid_value("1")
    assert val.is_valid_value("1,2")
    val = validators.IntListValidator(allow_single=False)
    assert not val.is_valid_value("1")
    assert val.is_valid_value("1,2")
    repr(val)
    assert val != validators.PathValidator()
    assert val == validators.IntListValidator(allow_single=False)


def test_floatlistvalidator():
    val = validators.FloatListValidator(allow_single=True)
    assert val.is_valid_value("1.0")
    assert val.is_valid_value("1.0,2")
    val = validators.FloatListValidator(allow_single=False)
    assert not val.is_valid_value("1.0")
    assert val.is_valid_value("1.0,2")
    repr(val)
    assert val != validators.PathValidator()
    assert val == validators.FloatListValidator(allow_single=False)


def test_regexpatternvalidator():
    val = validators.RegexPatternValidator()
    assert val.is_valid_value("[") is False
    assert val.is_valid_value("[0-9]") is True
    repr(val)
    assert val != validators.PathValidator()
    assert val == validators.RegexPatternValidator()


def test_colorvalidator():
    val = validators.ColorValidator()
    state, text, pos = val.validate("", 0)
    assert state == val.State.Intermediate
    assert (text, pos) == ("", 0)
    state, _, _ = val.validate("notacolor", 3)
    assert state == val.State.Intermediate
    assert val.is_valid_value("#ff0000")
    assert val.is_valid_value("red")


def test_monotoniclistvalidator_decreasing():
    val = validators.MonotonicListValidator(kind="decreasing")
    expected_pos = 8
    state, text, pos = val.validate("10, 5, 1", expected_pos)
    assert state == val.State.Acceptable
    assert text == "10, 5, 1"
    assert pos == expected_pos
    state, text, _ = val.validate("1, 5, 10", expected_pos)
    assert state == val.State.Intermediate
    assert text == "1, 5, 10"


def test_integervalidator():
    val = validators.IntegerValidator(bottom=-10, top=10)
    assert val.validate("--5", 2)[0] == val.State.Invalid
    assert val.validate("²", 1)[0] == val.State.Invalid
    state, text, pos = val.validate("5", 0)
    assert state == val.State.Acceptable
    assert (text, pos) == ("5", 0)
    state, _, pos = val.validate("-", 1)
    assert state == val.State.Intermediate
    assert pos == 1


def test_scientificfloatvalidator():
    val = validators.ScientificFloatValidator()
    # position beyond length must not raise IndexError
    state, _, _ = val.validate("abc", 99)
    assert state == val.State.Invalid
    # "+." and ".-" must not be treated as single-char intermediate
    assert val.validate("+.", 2)[0] == val.State.Intermediate
    assert val.validate(".-", 2)[0] == val.State.Intermediate
    assert val.validate("1.5e-3", 6)[0] == val.State.Acceptable


def test_baseregexvalidator_pickle_and_intlist():
    val = validators.regexvalidators.BaseRegexValidator(regex=r"\d+")
    restored = pickle.loads(pickle.dumps(val))
    assert restored == val
    assert restored.is_valid_value("123")
    assert not restored.is_valid_value("abc")

    int_list = validators.IntListValidator(allow_single=False)
    assert not int_list.is_valid_value("12")
    assert not int_list.is_valid_value("1,,2")
    assert int_list.is_valid_value("1,2")
    assert int_list.is_valid_value("10,20,30")


def test_hexvalidator():
    val = validators.HexValidator(maximum=0xFF)
    assert val.is_valid_value("ff")
    assert val.is_valid_value("0xff")
    assert not val.is_valid_value("0b10")
    assert not val.is_valid_value("0o10")
    assert val.validate("100", 3)[0] == val.State.Invalid


def test_pathvalidator_edge_cases():
    val = validators.PathValidator()
    assert val.validate("", 0)[0] == val.State.Intermediate
    assert val.validate("\x00", 1)[0] in (val.State.Intermediate, val.State.Invalid)


def test_textlengthvalidator_preserves_pos():
    val = validators.TextLengthValidator(minimum=2, maximum=5)
    assert val.validate("abc", 1) == (val.State.Acceptable, "abc", 1)
    assert val.validate("a", 0) == (val.State.Intermediate, "a", 0)
    assert val.validate("abcdef", 3) == (val.State.Invalid, "abcdef", 3)
