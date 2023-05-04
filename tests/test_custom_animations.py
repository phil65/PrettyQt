"""Tests for `prettyqt` package."""

from prettyqt import custom_animations, widgets


def test_bounceanimation(qtbot):
    anim = custom_animations.BounceAnimation()
    widget = widgets.Widget()
    anim.set_start_value((20, 20))
    anim.set_end_value((20, 20))
    anim.set_duration(40)
    anim.apply_to(widget)


def test_fadeanimation(qtbot):
    anim = custom_animations.FadeInAnimation()
    widget = widgets.Widget()
    anim.apply_to(widget)


def test_slideanimation(qtbot):
    anim = custom_animations.SlideAnimation()
    anim.set_start_value((20, 20))
    anim.set_end_value((20, 20))
    widget = widgets.Widget()
    anim.apply_to(widget)
