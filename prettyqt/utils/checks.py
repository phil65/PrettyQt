"""Module containing functions and decorators for validity checking."""

import functools
import logging
from collections.abc import Callable

from prettyqt import core, widgets

logger = logging.getLogger(__name__)


def ci(
    index_is_valid: bool = False,
    do_not_use_parent: bool = False,
    parent_is_invalid: bool = False,
):
    def inner(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(
            ref: widgets.AbstractItemModelMixin, index: core.QModelIndex, *args, **kwargs
        ):
            if ref.check_index(
                index, index_is_valid, do_not_use_parent, parent_is_invalid
            ):
                return fn(ref, index, *args, **kwargs)
            else:
                raise TypeError("Invalid index")

        return wrapper

    return inner


def requires_model(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def wrapper(ref: widgets.AbstractItemViewMixin, *args, **kwargs):
        if ref.model() is None:
            raise RuntimeError(f"Trying to call {fn.__name__} without a model set.")
        return fn(ref, *args, **kwargs)

    return wrapper
