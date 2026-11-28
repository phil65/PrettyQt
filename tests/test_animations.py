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


def test_textanimation_color(qtbot):
    from prettyqt import core, gui, widgets

    label = widgets.Label()
    qtbot.addWidget(label)
    anim = animations.TextAnimation(parent=label)
    assert anim.endValue() == ""
    anim.apply_to(label.text)
    anim.start()
    anim.updateCurrentValue(gui.QColor("red"))
    anim.updateCurrentValue(1.5)
    anim.updateCurrentValue(core.QPoint(3, 4))
    assert label.text() == "3, 4"
    anim.updateCurrentValue(core.QSize(10, 20))
    assert label.text() == "10, 20"
    anim.stop()


def test_zoomanimation_math_and_no_parent(qtbot):
    from prettyqt import core

    widget = widgets.Widget()
    qtbot.addWidget(widget)
    widget.resize(100, 80)
    widget.move(50, 40)

    anim = animations.ZoomAnimation(start=1.0, end=2.0, anchor="center")
    anim.apply_to(widget)
    anim.set_start_value(1.0)
    anim.set_end_value(2.0)
    assert anim.anim1.endValue() == core.QSize(200, 160)
    assert anim.anim2.endValue() == core.QPoint(0, 0)


def test_flasheffect_no_parent_and_args(qtbot):
    from prettyqt import gui
    from prettyqt.animations import flasheffect

    effect = flasheffect.FlashEffect(duration=250, color="blue")
    assert effect._flash_animation.duration() == 250  # noqa: PLR2004
    assert effect._flash_animation.keyValueAt(0.1) == gui.QColor("blue")


def test_fx_highlight_widget(qtbot):
    container = widgets.Widget()
    qtbot.addWidget(container)
    child = widgets.PushButton("hi", parent=container)
    overlay = container.fx.highlight_widget(child)
    assert overlay is not None
    assert overlay.parent() is container
