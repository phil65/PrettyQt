import annotationlib
import functools
import inspect
import itertools
import logging
from typing import TYPE_CHECKING, Any, Optional, get_args

from prettyqt.qt import QtCore


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    import types


logger = logging.getLogger(__name__)


def Slot(
    *args: Any,
    auto: bool = False,
    trace: bool = False,
    span_name: str | None = None,
    **kwargs: Any,
):
    if auto:
        return AutoSlot

    def outer_decorator(fn):
        target = fn
        if trace:
            from prettyqt import telemetry

            target = telemetry.traced_slot(span_name)(target)
        if inspect.iscoroutinefunction(target):

            @QtCore.Slot(*args, **kwargs)
            @functools.wraps(fn)
            def wrapper(*call_args, **call_kwargs):
                from prettyqt.core import aio

                return aio.schedule_coroutine(target(*call_args, **call_kwargs))

            return wrapper
        return QtCore.Slot(*args, **kwargs)(target)

    return outer_decorator


def is_optional(typ) -> bool:
    return typ in (Optional, type(Optional))


# def is_optional(field):
#     return get_origin(field) is Union and type(None) in typing.get_args(field)


def get_optional_args(annotations: Iterable[Any]) -> list[Any]:
    return [get_args(arg)[0] for arg in annotations if is_optional(arg)]


def get_concrete(annotation: Any) -> type | None:
    return getattr(annotation, "__origin__", None)


def get_concretes(annotations: list) -> list:
    ret = []
    for item in annotations:
        if is_optional(item):
            annotations.remove(item)
            continue
        if concrete := get_concrete(item):
            ret.append(concrete)
            annotations.remove(item)
    return ret + annotations


def _resolve_annotation(annotation: Any) -> Any:
    """Map an annotation that cannot be evaluated (TYPE_CHECKING-only) to `object`."""
    if isinstance(annotation, annotationlib.ForwardRef):
        return object
    return annotation


def _get_slot_annotations(func: Callable) -> dict[str, Any]:
    """Read annotations without evaluating names that only exist for type checkers.

    A fresh dict, so the function's own `__annotations__` stay untouched.
    """
    annotations = annotationlib.get_annotations(
        func, format=annotationlib.Format.FORWARDREF
    )
    return {k: _resolve_annotation(v) for k, v in annotations.items()}


def AutoSlot(func):
    def wrapper(func):
        anots = _get_slot_annotations(func)
        return_ = anots.pop("return", None)
        if return_ is type(None):
            return_ = None
        if return_ is Any:
            return_ = "QVariant"
        result = {} if return_ is None else {"result": return_}
        args = list(anots.values())
        stripped_optionals = get_concretes(get_optional_args(args))
        concretes = get_concretes(args)
        if stripped_optionals:
            required_annotations = tuple(concretes)
            combos = [
                subset
                for i in range(len(stripped_optionals) + 1)
                for subset in itertools.combinations(stripped_optionals, i)
            ]
            for combo in combos:
                func = QtCore.Slot(*combo + required_annotations, **result)(func)
            return func
        return QtCore.Slot(*concretes, **result)(func)

    return wrapper(func)


class _OverloadedSlotPlaceholder:
    def __init__(self, name, original_name):
        self.name = name
        self.original_name = original_name

    def __repr__(self):
        return f"<placeholder slot {self.name} for {self.original_name}>"


def _build_arguments(
    func: types.FunctionType, original_func: types.FunctionType | None = None
) -> tuple[list, dict]:
    signature = inspect.signature(func, annotation_format=annotationlib.Format.FORWARDREF)
    args = [
        p.name
        for p in signature.parameters.values()
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    annotations = _get_slot_annotations(func)

    slot_args: list[Any] = []
    slot_kwargs: dict[str, Any] = {}

    if "return" in annotations and annotations["return"] is not None:
        slot_kwargs["result"] = annotations["return"]

    if original_func and func.__name__ != original_func.__name__:
        slot_kwargs["name"] = func.__name__

    gap = False

    for index, arg in enumerate(args):
        # Let the first arg pass by unannotated, as it may be the 'self'
        # argument of a function. Static methods can't be used as slots anyways
        if index == 0 and arg not in annotations:
            continue

        if arg in annotations and not gap:
            slot_args.append(annotations[arg])
        elif arg not in annotations:
            gap = True
        else:
            msg = (
                f"Annotations must be in a continuous row - arg before '{arg}' is missing"
            )
            raise TypeError(msg)

    return slot_args, slot_kwargs


def AutoSlotAlternative(func: types.FunctionType):
    """A special slot decorator using function annotations to provide the argument types.

    Use like so:

        @slot
        def my_function(self, x: int, y: int) -> int:
            return x ** y

    You can also overload a function by doing this:

        @slot
        def overloaded_func(self, output=None: str):
            print(output)

        @overloaded_func.overload
        def overloaded_func(self, output: int): ...

        # And an overload for calling it with no arguments, so it will fall back
        # on the default argument.
        @overloaded_func.overload
        def overloaded_func(self): ...

    Note: you cannot set different default arguments in the overloads, you may
    only set a function's default arguments in the main declaration.

    The function body on overloads is completely ignored, so you can just use
    ellipses (`...`) or `pass` to fill in the body.
    """
    args, kwargs = _build_arguments(func)
    logger.debug("Auto-slot for %s: args: %s, kwargs: %s", func.__name__, args, kwargs)

    QtCore.Slot(*args, **kwargs)(func)

    def overload(new_func):
        args, kwargs = _build_arguments(new_func, func)

        QtCore.Slot(*args, **kwargs)(func)

        if new_func.__name__ != func.__name__:
            return _OverloadedSlotPlaceholder(new_func.__name__, func.__name__)
        return func

    func.overload = overload  # type: ignore

    return func
