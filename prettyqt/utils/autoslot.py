# Functions for the Qt meta-object system (like signal, slot, etc)
# credits to Empyrical
# https://gist.github.com/empyrical/a103c46f454a433e8798#file-decorator-py

from __future__ import annotations

import inspect
import logging
from typing import Callable, get_type_hints

from prettyqt import core


logger = logging.getLogger(__name__)


class _OverloadedSlotPlaceholder:
    def __init__(self, name, original_name):
        self.name = name
        self.original_name = original_name

    def __repr__(self):
        return f"<placeholder slot {self.name} for function {self.original_name}>"


def _build_arguments(
    func: Callable, original_func: Callable | None = None
) -> tuple[list, dict]:
    argspec = inspect.getfullargspec(func)
    args = argspec.args
    annotations = get_type_hints(func)

    slot_args = []
    slot_kwargs = {}

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
        elif arg in annotations and gap:
            raise TypeError(
                "Type annotations must be in a continuous row - an argument "
                f'before "{arg}" is missing'
            )

    return slot_args, slot_kwargs


def AutoSlot(func: Callable):
    """A special slot decorator using function annotations to provide the argument types.

    It's just syntactic sugar for the slot decorators that already come with the
    Python Qt bindings.

    This has **no effect whatsoever** on the Python side of things - it does not
    do type checking, it only registers a function and the types its arguments
    take with Qt's Meta Object system.

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
    logger.debug(f"Auto-slot for {func.__name__}: args: {args}, kwargs: {kwargs}")

    core.Slot(*args, **kwargs)(func)

    def overload(new_func):
        args, kwargs = _build_arguments(new_func, func)

        core.Slot(*args, **kwargs)(func)

        if new_func.__name__ != func.__name__:
            return _OverloadedSlotPlaceholder(new_func.__name__, func.__name__)
        else:
            return func

    func.overload = overload  # type: ignore

    return func
