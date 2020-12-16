"""Tests for `prettyqt` package."""

import pytest

from prettyqt import core, webenginecore
from prettyqt.utils import InvalidParamError


def test_webengineurlscheme():
    scheme = webenginecore.WebEngineUrlScheme()
    scheme.set_name("test")
    assert scheme.get_name() == "test"
    scheme.set_syntax("host")
    with pytest.raises(InvalidParamError):
        scheme.set_syntax("test")
    assert scheme.get_syntax() == "host"


def test_webenginehttprequest():
    req = webenginecore.WebEngineHttpRequest()
    headers = {"a": "b"}
    req.set_headers(headers)
    assert req.get_headers() == headers
    req.set_method("post")
    with pytest.raises(InvalidParamError):
        req.set_method("test")
    assert req.get_method() == "post"
    req.set_url("http://www.google.de")
    assert req.get_url() == core.Url("http://www.google.de")
    req.get_post_data()
