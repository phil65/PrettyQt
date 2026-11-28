from typing import TYPE_CHECKING, Literal

from prettyqt import widgets
from prettyqt.utils import bidict


mod = widgets.QGestureRecognizer

ResultFlagStr = Literal[
    "ignore",
    "may_be_gesture",
    "trigger_gesture",
    "finish_gesture",
    "cancel_gesture",
    "consume_event_hint",
]

RESULT_FLAG: bidict[ResultFlagStr, mod.ResultFlag] = bidict(
    ignore=mod.ResultFlag.Ignore,
    may_be_gesture=mod.ResultFlag.MayBeGesture,
    trigger_gesture=mod.ResultFlag.TriggerGesture,
    finish_gesture=mod.ResultFlag.FinishGesture,
    cancel_gesture=mod.ResultFlag.CancelGesture,
    consume_event_hint=mod.ResultFlag.ConsumeEventHint,
)


if TYPE_CHECKING:
    from prettyqt.qt import QtWidgets

    _GestureRecognizerBase = QtWidgets.QGestureRecognizer
else:
    _GestureRecognizerBase = object


class GestureRecognizerMixin(_GestureRecognizerBase):
    pass


class GestureRecognizer(GestureRecognizerMixin, widgets.QGestureRecognizer):
    """Provides the infrastructure for gesture recognition."""
