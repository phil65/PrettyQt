"""Tests for `prettyqt.prettyqtmarkdown`."""

import pytest

from prettyqt import core, gui, widgets


mknodes = pytest.importorskip("mknodes")
prettyqtmarkdown = pytest.importorskip("prettyqt.prettyqtmarkdown")


def test_markdown_widget_and_invalid_index(qtbot):
    page = mknodes.MkPage()
    page += mknodes.MkAdmonition("hello world")

    widget = prettyqtmarkdown.MarkdownWidget()
    qtbot.addWidget(widget)
    widget.set_markdown(page)

    model = widget.tree.model()
    assert isinstance(model, prettyqtmarkdown.MkNodesModel)
    assert model.rowCount() >= 1

    # Invalid ModelIndex must be ignored cleanly
    widget._on_current_change(core.ModelIndex(), core.ModelIndex())

    # Valid ModelIndex populates the code editor with rendered markdown
    first_index = model.index(0, 0)
    assert first_index.isValid()
    widget._on_current_change(first_index, core.ModelIndex())
    assert len(widget.textbox.text()) > 0


def test_mk_widget_screenshot_resize_to(qapp):
    btn = widgets.PushButton("Test")
    screenshot = prettyqtmarkdown.MkWidgetScreenShot(btn, resize_to=(120, 40))

    assert screenshot.path == "PushButton_screenshot.png"
    assert screenshot.data.startswith(b"\x89PNG\r\n\x1a\n")

    image = gui.Image.fromData(screenshot.data, "PNG")
    assert not image.isNull()
    dpr = btn.devicePixelRatio()
    assert btn.size() == core.QSize(120, 40)
    assert image.size() == core.QSize(round(120 * dpr), round(40 * dpr))
