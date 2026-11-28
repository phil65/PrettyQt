"""Composable, binding-agnostic hooks for Qt signal connections and emissions.

Provides a single point of interception for `SignalInstance.connect`,
`SignalInstance.disconnect`, and `SignalInstance.emit` so features such as
async slot scheduling and OpenTelemetry instrumentation can compose cleanly
without clobbering each other or breaking Qt semantics:

- Preserves Qt's automatic argument-count trimming (e.g. `clicked(bool)` -> `fn()`).
- Uses weak references for `QObject` bound methods so connections never leak QObjects.
- Keeps a weak registry of wrapped slots so `signal.disconnect(original_slot)` works.
- Restores the original `SignalInstance` methods completely when no hooks are active.
"""

import contextlib
import dataclasses
import functools
import inspect
import logging
import re
import types
from typing import TYPE_CHECKING, Any, Protocol
import weakref

from prettyqt.qt import QtCore


if TYPE_CHECKING:
    from collections.abc import Callable


logger = logging.getLogger(__name__)

_PYSIDE_REPR_RE = re.compile(r"SignalInstance\s+([^\s>]+)")
_PYQT_REPR_RE = re.compile(r"PYQT_SIGNAL\s+(\w+)\s+of\s+(\w+)")


@dataclasses.dataclass(frozen=True, slots=True)
class SignalInfo:
    """Metadata extracted from a Qt bound signal (`SignalInstance`)."""

    name: str
    signature: str
    sender_type: str | None = None


def get_signal_info(signal_instance: Any) -> SignalInfo:
    """Extract name, signature, and (when available) sender class from a signal."""
    raw_sig = getattr(signal_instance, "signal", None)
    rep = repr(signal_instance)
    if isinstance(raw_sig, str):
        # PyQt6 prefixes signal signatures with Qt's SIGNAL() macro code ("2").
        signature = raw_sig[1:] if raw_sig[:1].isdigit() else raw_sig
        name = signature.split("(", 1)[0]
        sender_type = None
        if match := _PYQT_REPR_RE.search(rep):
            sender_type = match.group(2)
        return SignalInfo(name=name, signature=signature, sender_type=sender_type)

    if match := _PYSIDE_REPR_RE.search(rep):
        signature = match.group(1)
        name = signature.split("(", 1)[0]
        return SignalInfo(name=name, signature=signature)

    return SignalInfo(name=rep, signature=rep)


def get_callable_name(fn: Callable[..., Any]) -> str:
    """Return a human-readable qualified name for a callable."""
    if isinstance(fn, functools.partial):
        return f"partial({get_callable_name(fn.func)})"
    qualname = getattr(fn, "__qualname__", None) or getattr(fn, "__name__", None)
    if qualname:
        module = getattr(fn, "__module__", None)
        if module and module not in {"builtins", "__main__"}:
            return f"{module}.{qualname}"
        return str(qualname)
    return type(fn).__qualname__


_UNSET = object()


def max_positional_args(fn: Callable[..., Any]) -> int | None:
    """Return the max positional arg count for `fn`, or `None` if unbounded."""
    if (val := getattr(fn, "_prettyqt_max_args", _UNSET)) is not _UNSET:
        return val if isinstance(val, int) or val is None else None
    try:
        sig = inspect.signature(fn)
    except ValueError, TypeError:
        return None
    count = 0
    for param in sig.parameters.values():
        if param.kind is inspect.Parameter.VAR_POSITIONAL:
            return None
        if param.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            count += 1
    return count


def is_wrappable_slot(slot: Any) -> bool:
    """Return whether `slot` can safely be wrapped by a Python hook.

    Skips signal-to-signal connections (`SignalInstance`) and C++ Qt builtin
    methods (whose signatures may be unavailable in PyQt6 and which benefit from
    direct C++-to-C++ dispatch).
    """
    if not callable(slot):
        return False
    if isinstance(slot, QtCore.SignalInstance):
        return False
    if isinstance(slot, types.BuiltinFunctionType | types.BuiltinMethodType):
        self_obj = getattr(slot, "__self__", None)
        if isinstance(self_obj, QtCore.QObject):
            return False
        # Skip other C builtins without an inspectable Python signature.
        try:
            inspect.signature(slot)
        except ValueError, TypeError:
            return False
    return True


def make_safe_slot_wrapper(
    slot: Callable[..., Any],
    invoker: Callable[[Callable[..., Any], tuple[Any, ...]], Any],
) -> Callable[..., Any]:
    """Create a Qt-safe wrapper around `slot` delegating calls to `invoker`.

    - Trims excess signal arguments to match Qt's slot invocation rules.
    - Uses `weakref.WeakMethod` for bound methods of `QObject` instances so the
      wrapper does not prevent garbage collection of widgets/QObjects.
    - When `slot` is a coroutine function and `invoker` is also a coroutine
      function, returns a coroutine function so downstream hooks (such as
      `AsyncSlotHook`) can still recognize and schedule it.
    """
    max_args = max_positional_args(slot)
    is_qobject_method = isinstance(slot, types.MethodType) and isinstance(
        slot.__self__, QtCore.QObject
    )
    weak_method: weakref.WeakMethod[Any] | None = (
        weakref.WeakMethod(slot) if is_qobject_method else None
    )
    strong_slot: Callable[..., Any] | None = None if is_qobject_method else slot

    if inspect.iscoroutinefunction(slot) and inspect.iscoroutinefunction(invoker):

        async def async_wrapper(*args: Any) -> Any:
            target = weak_method() if weak_method is not None else strong_slot
            if target is None:
                return None
            trimmed = args if max_args is None else args[:max_args]
            return await invoker(target, trimmed)

        async_wrapper.__name__ = getattr(slot, "__name__", "wrapped_slot")
        async_wrapper.__qualname__ = getattr(slot, "__qualname__", async_wrapper.__name__)
        async_wrapper._prettyqt_original_slot = (  # ty: ignore[missing-attribute]
            slot if not is_qobject_method else weak_method
        )
        async_wrapper._prettyqt_max_args = max_args  # ty: ignore[missing-attribute]
        return async_wrapper

    def wrapper(*args: Any) -> Any:
        target = weak_method() if weak_method is not None else strong_slot
        if target is None:
            return None
        trimmed = args if max_args is None else args[:max_args]
        return invoker(target, trimmed)

    wrapper.__name__ = getattr(slot, "__name__", "wrapped_slot")
    wrapper.__qualname__ = getattr(slot, "__qualname__", wrapper.__name__)
    wrapper._prettyqt_original_slot = slot if not is_qobject_method else weak_method  # ty: ignore[missing-attribute]
    wrapper._prettyqt_max_args = max_args  # ty: ignore[missing-attribute]
    return wrapper


def _slot_key(slot: Any) -> Any:
    """Stable hashable key for a slot without holding a strong reference."""
    if isinstance(slot, types.MethodType):
        return (id(slot.__self__), id(slot.__func__))
    return id(slot)


def _signal_key(signal_instance: Any, info: SignalInfo) -> tuple[int, str]:
    return (hash(signal_instance), info.signature)


class SignalHook(Protocol):
    """Protocol implemented by signal-slot hooks registered on `SignalHookManager`."""

    def wrap_slot(
        self, signal_info: SignalInfo, slot: Callable[..., Any]
    ) -> Callable[..., Any] | None:
        """Return a wrapped callable for `slot`, or `None` to leave it unchanged."""
        ...

    def on_emit(
        self, signal_info: SignalInfo, args: tuple[Any, ...]
    ) -> contextlib.AbstractContextManager[Any] | None:
        """Optional context manager entered around Python-initiated `signal.emit()`."""
        ...


class SignalHookManager:
    """Manages composable hooks on Qt's `SignalInstance`."""

    def __init__(self) -> None:
        self._hooks: list[SignalHook] = []
        self._installed: bool = False
        self._orig_connect: Any = None
        self._orig_disconnect: Any = None
        self._orig_emit: Any = None
        # (hash(signal), signature) -> {slot_key: [weakref.ref(wrapped_slot), ...]}
        self._wrapped: dict[tuple[int, str], dict[Any, list[weakref.ref[Any]]]] = {}

    @property
    def active(self) -> bool:
        return self._installed

    @property
    def hooks(self) -> tuple[SignalHook, ...]:
        return tuple(self._hooks)

    def register(self, hook: SignalHook) -> None:
        """Register a hook, patching `SignalInstance` on first registration.

        Hooks are ordered by their optional `priority` attribute (lower runs
        first, default 50) so e.g. telemetry wraps coroutine bodies before
        async slot schedulers convert them into sync task launchers.
        """
        if hook in self._hooks:
            return
        self._hooks.append(hook)
        self._hooks.sort(key=lambda h: getattr(h, "priority", 50))
        if not self._installed:
            self._install()

    def unregister(self, hook: SignalHook) -> None:
        """Unregister a hook, restoring `SignalInstance` when none remain."""
        if hook not in self._hooks:
            return
        self._hooks.remove(hook)
        if not self._hooks and self._installed:
            self._uninstall()

    def _install(self) -> None:
        sig_cls = QtCore.SignalInstance
        orig_connect = sig_cls.connect
        orig_disconnect = sig_cls.disconnect
        orig_emit = sig_cls.emit
        manager = self

        def patched_connect(sig_self: Any, slot: Any, *args: Any, **kwargs: Any) -> Any:
            if not manager._hooks or not is_wrappable_slot(slot):
                return orig_connect(sig_self, slot, *args, **kwargs)
            info = get_signal_info(sig_self)
            current = slot
            for hook in manager._hooks:
                wrapped = hook.wrap_slot(info, current)
                if wrapped is not None:
                    current = wrapped
            conn = orig_connect(sig_self, current, *args, **kwargs)
            if current is not slot:
                manager._record_wrapped(sig_self, info, slot, current)
            return conn

        def patched_disconnect(sig_self: Any, *args: Any, **kwargs: Any) -> Any:
            info = get_signal_info(sig_self)
            s_key = _signal_key(sig_self, info)
            if not args and not kwargs:
                manager._wrapped.pop(s_key, None)
                return orig_disconnect(sig_self)
            target = args[0] if args else None
            if target is not None and not isinstance(
                target, QtCore.QMetaObject.Connection
            ):
                wrapped = manager._pop_wrapped(s_key, target)
                if wrapped is not None:
                    return orig_disconnect(sig_self, wrapped, *args[1:], **kwargs)
            return orig_disconnect(sig_self, *args, **kwargs)

        def patched_emit(sig_self: Any, *args: Any) -> Any:
            hooks = manager._hooks
            if not hooks:
                return orig_emit(sig_self, *args)
            cms: list[contextlib.AbstractContextManager[Any]] = []
            info: SignalInfo | None = None
            for hook in hooks:
                if hasattr(hook, "on_emit"):
                    if info is None:
                        info = get_signal_info(sig_self)
                    cm = hook.on_emit(info, args)
                    if cm is not None:
                        cms.append(cm)
            if not cms:
                return orig_emit(sig_self, *args)
            with contextlib.ExitStack() as stack:
                for cm in cms:
                    stack.enter_context(cm)
                return orig_emit(sig_self, *args)

        try:
            sig_cls.connect = patched_connect
            sig_cls.disconnect = patched_disconnect
            sig_cls.emit = patched_emit
        except TypeError:
            logger.debug("Binding %s does not allow patching SignalInstance", sig_cls)
            return

        self._orig_connect = orig_connect
        self._orig_disconnect = orig_disconnect
        self._orig_emit = orig_emit
        self._installed = True

    def _uninstall(self) -> None:
        if not self._installed:
            return
        sig_cls = QtCore.SignalInstance
        sig_cls.connect = self._orig_connect
        sig_cls.disconnect = self._orig_disconnect
        sig_cls.emit = self._orig_emit
        self._orig_connect = None
        self._orig_disconnect = None
        self._orig_emit = None
        self._installed = False
        self._wrapped.clear()

    def _record_wrapped(
        self,
        signal_instance: Any,
        info: SignalInfo,
        original_slot: Any,
        wrapped_slot: Any,
    ) -> None:
        s_key = _signal_key(signal_instance, info)
        slot_k = _slot_key(original_slot)
        per_sig = self._wrapped.setdefault(s_key, {})
        entries = per_sig.setdefault(slot_k, [])
        # Prune dead weakrefs opportunistically.
        entries[:] = [ref for ref in entries if ref() is not None]
        entries.append(weakref.ref(wrapped_slot))

    def _pop_wrapped(self, s_key: tuple[int, str], original_slot: Any) -> Any | None:
        per_sig = self._wrapped.get(s_key)
        if not per_sig:
            return None
        slot_k = _slot_key(original_slot)
        entries = per_sig.get(slot_k)
        if not entries:
            return None
        while entries:
            ref = entries.pop()
            if (target := ref()) is not None:
                if not entries:
                    per_sig.pop(slot_k, None)
                    if not per_sig:
                        self._wrapped.pop(s_key, None)
                return target
        per_sig.pop(slot_k, None)
        if not per_sig:
            self._wrapped.pop(s_key, None)
        return None


_hook_manager = SignalHookManager()


def get_hook_manager() -> SignalHookManager:
    """Return the process-wide `SignalHookManager` singleton."""
    return _hook_manager
