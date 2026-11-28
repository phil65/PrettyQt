"""Tests for `prettyqt.custom_network`."""

from prettyqt.custom_network import googlecompleter, update_check


def test_update_checker_none_urls_do_not_fetch(qapp, monkeypatch):
    called_urls: list[str] = []

    checker_packaged = update_check.UpdateChecker(
        app_name="test",
        app_version="1.0.0",
        releases_url=None,
        packaged=True,
    )
    monkeypatch.setattr(
        checker_packaged, "get", lambda url, timeout=30: called_urls.append(url)
    )
    checker_packaged.check_for_update()
    assert called_urls == []

    checker_pypi = update_check.UpdateChecker(
        app_name="test",
        app_version="1.0.0",
        pypi_url=None,
        packaged=False,
    )
    monkeypatch.setattr(
        checker_pypi, "get", lambda url, timeout=30: called_urls.append(url)
    )
    checker_pypi.check_for_update()
    assert called_urls == []


def test_update_checker_builds_expected_urls(qapp, monkeypatch):
    called_urls: list[str] = []

    checker_packaged = update_check.UpdateChecker(
        app_name="test",
        app_version="1.0.0",
        releases_url="https://example.com/releases",
        packaged=True,
    )
    monkeypatch.setattr(
        checker_packaged, "get", lambda url, timeout=30: called_urls.append(url)
    )
    checker_packaged.check_for_update()
    assert called_urls == ["https://example.com/releases.atom"]

    called_urls.clear()
    checker_pypi = update_check.UpdateChecker(
        app_name="test",
        app_version="1.0.0",
        pypi_url="https://example.com/pypi/prettyqt",
        packaged=False,
    )
    monkeypatch.setattr(
        checker_pypi, "get", lambda url, timeout=30: called_urls.append(url)
    )
    checker_pypi.check_for_update()
    assert called_urls == ["https://example.com/pypi/prettyqt/json"]


def test_update_checker_parses_offline_responses(qtbot):
    checker_packaged = update_check.UpdateChecker(
        app_name="test",
        app_version="9.9.9",
        packaged=True,
    )
    with qtbot.waitSignal(checker_packaged.version_checked, timeout=1000) as blocker:
        checker_packaged._on_download_finished(
            b'<link href="https://github.com/org/repo/releases/tag/v1.2.3"/>',
            "https://example.com/releases.atom",
        )
    assert blocker.args == ["1.2.3"]

    checker_pypi = update_check.UpdateChecker(
        app_name="test",
        app_version="9.9.9",
        packaged=False,
    )
    with qtbot.waitSignal(checker_pypi.version_checked, timeout=1000) as blocker:
        checker_pypi._on_download_finished(
            b'{"info": {"version": "2.4.6"}}',
            "https://example.com/pypi/prettyqt/json",
        )
    assert blocker.args == ["2.4.6"]

    # Unparseable payload does not raise or emit
    emitted: list[str] = []
    checker_pypi.version_checked.connect(emitted.append)
    checker_pypi._on_download_finished(b"no version here", "https://example.com")
    assert emitted == []


def test_google_search_model_offline(qapp):
    model = googlecompleter.GoogleSearchModel()
    assert model.rowCount() == 0

    # Empty search clears without making a network request
    model.search("")
    assert model.rowCount() == 0

    xml = (
        '<?xml version="1.0"?>'
        "<toplevel>"
        '<CompleteSuggestion><suggestion data="prettyqt"/></CompleteSuggestion>'
        '<CompleteSuggestion><suggestion data="pyqt6"/></CompleteSuggestion>'
        "</toplevel>"
    )
    assert model.process_reply(xml) == ["prettyqt", "pyqt6"]
