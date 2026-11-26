"""Tests for the annotation-driven slot decorators."""

import annotationlib
from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.core.slot import AutoSlot, AutoSlotAlternative


if TYPE_CHECKING:
    from prettyqt import widgets


def _slot_signatures(obj: core.QObject) -> set[str]:
    meta = obj.metaObject()
    return {
        bytes(meta.method(i).methodSignature()).decode()
        for i in range(meta.methodOffset(), meta.methodCount())
    }


def test_autoslot_with_type_checking_only_annotation(qapp):
    class Receiver(core.QObject):
        @AutoSlot
        def set_value(self, value: int, widget: widgets.Widget) -> None:
            pass

    signatures = _slot_signatures(Receiver())
    assert len(signatures) == 1
    assert next(iter(signatures)).startswith("set_value(int,")
    # The function's own annotations are left untouched.
    fmt = annotationlib.Format.FORWARDREF
    assert "return" in annotationlib.get_annotations(Receiver.set_value, format=fmt)


def test_autoslot_alternative_with_type_checking_only_annotation(qapp):
    class Receiver(core.QObject):
        @AutoSlotAlternative
        def set_value(self, value: int, widget: widgets.Widget) -> None:
            pass

    signatures = _slot_signatures(Receiver())
    assert len(signatures) == 1
    assert next(iter(signatures)).startswith("set_value(int,")
