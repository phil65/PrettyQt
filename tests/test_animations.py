"""Tests for `prettyqt` package."""

from prettyqt import animations, widgets


def test_slideanimation(qtbot):
    widget = widgets.Widget()
    qtbot.addWidget(widget)
    anim = animations.SlideAnimation(parent=widget)
    anim.set_start_value((20, 20))
    anim.set_end_value((20, 20))
    anim.apply_to(widget)


def test_fx(qtbot):
    widget = widgets.Label("test")
    qtbot.add_widget(widget)
    widget.show()
    widget.fx["windowOpacity"].animate(start=0, end=1, duration=10)
    widget.fx["size"].transition_to((500, 500), duration=10)
    widget.fx.fade_in(duration=10)
    widget.fx.zoom(start=1, end=1.5, duration=10)
    widget.fx.slide(start=(0, 0), end=(100, 0), duration=10)
