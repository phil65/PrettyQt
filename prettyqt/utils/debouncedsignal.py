from __future__ import annotations

import time

from prettyqt import core
from prettyqt.qt import QtCore


class DebouncedSignal:
    """Signal definition.

    Instances of this class will be replaced with a QObject holding a SignalInstance
     by the SignalMeta metaclass.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class SignalMeta(type(QtCore.QObject)):
    def __new__(cls, name, bases, attrs, **kwargs):
        to_replace = {
            k: (v.args, v.kwargs)
            for k, v in attrs.items()
            if isinstance(v, DebouncedSignal)
        }
        new_cls = super().__new__(cls, name, bases, attrs, **kwargs)
        user_init = new_cls.__init__

        def __init__(self, *args, **kwargs_):
            user_init(self, *args, **kwargs_)
            for k, v in to_replace.items():
                self.__dict__[k] = get_debounced_signal(*v[0], **v[1])()

        new_cls.__init__ = __init__
        return new_cls


class BaseSignalImpl(core.Object):
    def __getitem__(self, item: type | str):
        return self.signal[item]

    def __getattr__(self, attr):
        return getattr(self.signal, attr)

    def connect(self, slot_or_signal):
        if isinstance(slot_or_signal, BaseSignalImpl):
            self.signal.connect(slot_or_signal.signal)  # or .emit?
        else:
            self.signal.connect(slot_or_signal)

    # def __call__(self, *args, **kwargs):
    #     self.emit(*args)
    #     print("__call__", args)


def get_debounced_signal(
    *args: type | str,
    debounce_time: int | None = None,
    repeat_same: bool = True,
    **kwargs,
):
    class DebouncedSignalImpl(BaseSignalImpl):
        signal = core.Signal(*args)

        def __init__(self, *args):
            super().__init__()
            self.last_tried_emission = ...  # just a sentinel value
            self.debounce_time = debounce_time
            # self.last_emission_time = time.time()
            # self.last_emission_try = time.time()
            self.timer = core.Timer(timeout=self.timer_emit, single_shot=True)
            self.repeat_same = repeat_same

        def emit(self, *args):
            # now = time.time()
            # debounce_time = self.debounce_time or 0
            # should_emit = now - self.last_emission_time > debounce_time
            if (args != self.last_tried_emission) or self.repeat_same:
                if self.debounce_time:
                    self.timer.start(self.debounce_time)
                else:
                    self.signal.emit(*args)
            self.last_tried_emission = args
            # print("emitted", args)
            # self.last_emission_time = time.time()

        def timer_emit(self):
            self.signal.emit(*self.last_tried_emission)
            self.last_emission_time = time.time()
            # print("emitted delayed", self.last_tried_emission)

    return DebouncedSignalImpl


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    textedit = widgets.PlainTextEdit()

    class EmitPushButton(widgets.PushButton, metaclass=SignalMeta):
        btn_clicked_delayed = DebouncedSignal(str, debounce_time=1000, repeat_same=False)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.clicked.connect(self.on_click)

        def on_click(self):
            # self.btn_clicked.emit(self.text())
            self.btn_clicked_delayed.emit(str(self.text()))

    # print(SignalInstance.test)
    btn1 = EmitPushButton("Signal 1")
    btn2 = EmitPushButton("Signal 2")
    widget = widgets.Widget()
    widget.set_layout("vertical")
    widget.box.add(textedit)
    widget.box.add(btn1)
    widget.box.add(btn2)
    # textedit.value_changed.connect(btn2.btn_clicked_delayed.emit)
    btn1.btn_clicked_delayed.connect(textedit.appendPlainText)
    btn2.btn_clicked_delayed.connect(textedit.appendPlainText)
    widget.show()
    # a.number.signal.emit("test")
    with app.debug_mode():
        app.main_loop()
