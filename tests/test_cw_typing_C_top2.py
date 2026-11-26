# ruff: noqa: N999
"""Regression tests for runtime bugs discovered while type-checking custom_widgets."""

from prettyqt import constants, core, gui, widgets
from prettyqt.custom_widgets import (
    configwidget,
    cyclewidget,
    faderwidget,
    fuzzycompleter,
    notification,
    qobjectpropertiestableview,
    waitingspinner,
)


def test_faderwidget_connects_timeline_value_changed(qtbot):
    old_widget = widgets.Label("old")
    new_widget = widgets.Label("new")
    qtbot.addWidget(old_widget)
    qtbot.addWidget(new_widget)
    old_widget.resize(50, 30)
    new_widget.resize(50, 30)

    fader = faderwidget.FaderWidget(old_widget, new_widget, duration=50)
    qtbot.addWidget(fader)
    fader.timeline.valueChanged.emit(0.5)
    assert fader.pixmap_opacity == 0.5  # noqa: PLR2004
    fader.timeline.stop()


def test_waitingspinner_start_without_parent(qtbot):
    spinner = waitingspinner.WaitingSpinner()
    qtbot.addWidget(spinner)
    spinner.start()
    assert spinner.is_spinning()
    spinner.stop()
    assert not spinner.is_spinning()


def test_cyclewidget_accepts_generator_iterable(qtbot):
    widget = cyclewidget.CycleWidget(
        (str(i) for i in range(6)),
        core.QSize(40, 20),
    )
    qtbot.addWidget(widget)
    assert widget.origin_items == ["0", "1", "2", "3", "4", "5"]
    assert widget.count() == 12  # noqa: PLR2004

    widget.setItems(str(i) for i in range(3))
    assert widget.count() > 0


def test_configwidget_selection_setting_without_options(qtbot):
    window = configwidget.SettingsWindow()
    qtbot.addWidget(window)
    setting = configwidget.SelectionSetting(
        identifier="theme",
        label="Theme",
        description="Choose theme",
    )
    window.add_setting(setting)
    combos = window.configwidget.find_children(widgets.ComboBox)
    assert len(combos) == 1
    assert combos[0].count() == 0


def test_fuzzycompleter_enter_key_restores_self_completer(qtbot):
    combo = widgets.ComboBox()
    qtbot.addWidget(combo)
    completer = fuzzycompleter.FuzzyCompleter(combo)
    model = core.StringListModel(["alpha", "beta", "gamma"])
    completer.setModel(model)
    combo.setCompleter(completer)
    combo.setEditText("alpha")

    event = gui.QKeyEvent(
        core.QEvent.Type.KeyPress,
        constants.Key.Key_Enter,
        constants.KeyboardModifier.NoModifier,
    )
    completer.eventFilter(combo, event)
    assert combo.completer() is completer


def test_notification_area_remove_without_sender(qtbot):
    target = widgets.Widget()
    qtbot.addWidget(target)
    area = notification.NotificationArea(target)
    area.remove()


def test_qobjectpropertiestableview_unhook_without_model(qtbot):
    view = qobjectpropertiestableview.QObjectPropertiesTableView()
    qtbot.addWidget(view)
    view.unhook()

    obj = widgets.Widget()
    qtbot.addWidget(obj)
    view.set_qobject(obj, update_on_event=False)
    view.unhook()
