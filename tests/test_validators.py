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
