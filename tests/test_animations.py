"""Tests for `prettyqt` package."""

from prettyqt import animations, widgets


def test_slideanimation(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    anim = animations.SlideAnimation(parent=widget)
    anim.set_start_value((20, 20))
    anim.set_end_value((20, 20))
    anim.apply_to(widget)
