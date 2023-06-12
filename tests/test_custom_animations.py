"""Tests for `prettyqt` package."""

from prettyqt import custom_animations, widgets


def test_bounceanimation(qtbot):
    widget = widgets.Widget()
    anim = custom_animations.BounceAnimation(parent=widget)
    anim.set_start_value((20, 20))
    anim.set_end_value((20, 20))
    anim.set_duration(40)
    anim.apply_to(widget)


def test_fadeanimation(qtbot):
    widget = widgets.Widget()
    anim = custom_animations.FadeInAnimation(parent=widget)
    widget = widgets.Widget()
    anim.apply_to(widget)


def test_slideanimation(qtbot):
    widget = widgets.Widget()
    anim = custom_animations.SlideAnimation(parent=widget)
    anim.set_start_value((20, 20))
    anim.set_end_value((20, 20))
    widget = widgets.Widget()
    anim.apply_to(widget)
