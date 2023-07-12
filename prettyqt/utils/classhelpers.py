from __future__ import annotations

import collections

from collections.abc import Iterator
import contextlib
import functools
import importlib
import inspect
import logging
import operator
import types
import typing


T = typing.TypeVar("T", bound=type)


logger = logging.getLogger(__name__)

# def add_docs(klass):
#     import pathlib
#     from prettyqt import paths
#     klass_name = klass.__name__
#     qclass = klass
#     for k in klass.mro():
#         if k.__name__.startswith("Q"):
#             qclass = k
#             break
#     module = k.__module__.split(".")[1]
#     path = paths.DOCSTRING_PATH /  module
#     filepath = path / f"Q{klass_name.replace('Mixin', '')}.txt"
#     if filepath.exists():
#         klass.__doc__ =  filepath.read_text()
#     return klass


def lca_type(classes: list[type]) -> type:
    return next(
        iter(
            functools.reduce(
                operator.and_,
                (collections.Counter(Klass.mro()) for Klass in classes),
            )
        )
    )


def find_common_ancestor(cls_list: list[type]) -> type:
    mros = [list(inspect.getmro(cls)) for cls in cls_list]
    track = collections.defaultdict(int)
    while mros:
        for mro in mros:
            cur = mro.pop(0)
            track[cur] += 1
            if (
                track[cur] >= len(cls_list)
                and not cur.__name__.endswith("Mixin")
                and cur.__name__.startswith("Q")
            ):
                return cur
            if len(mro) == 0:
                mros.remove(mro)
    raise TypeError("Couldnt find common base class")


def get_subclasses(klass: type, include_abstract: bool = False) -> typing.Iterator[type]:
    if getattr(klass.__subclasses__, "__self__", None) is None:
        return
    for i in klass.__subclasses__():
        yield from get_subclasses(i)
        if include_abstract or not inspect.isabstract(i):
            yield i


def get_class_by_name(
    klass_name: str, *, parent_type: type = object, module_filter: list[str] | None = None
) -> type | None:
    return next(
        (
            kls
            for kls in get_subclasses(parent_type)
            if kls.__name__ == klass_name
            and (module_filter is None or kls.__module__.split(".")[0] in module_filter)
        ),
        None,
    )


def get_qt_parent_class(klass: type, only_direct: bool = False) -> type | None:
    """Get Qt-based parent class for given type.

    Arguments:
        klass: class to get parent type from
        only_direct: whether only the direct parent should be checked.
    """
    if only_direct:
        name = klass.mro()[0].__name__
        return klass if name.startswith(("PyQt", "PySide")) else None
    return next(
        (kls for kls in klass.mro() if kls.__module__.startswith(("PyQt", "PySide"))),
        None,
    )


def get_class_for_id(base_class: T, id_: str) -> T:
    """Get subclass of base class which has an attribute "ID" with given id.

    Arguments:
        base_class: Class to check subclasses from.
        id_: id to search for.
    """
    base_classes = (
        typing.get_args(base_class)
        if isinstance(base_class, types.UnionType)
        else (base_class,)
    )
    for base_class in base_classes:
        for Klass in get_subclasses(base_class):
            if "ID" in Klass.__dict__ and id_ == Klass.ID:
                logger.debug(f"found class for id {Klass.ID!r}")
                return Klass
    raise ValueError(f"Couldnt find class with id {id_!r} for base class {base_class}")


def iter_classes_for_module(
    module: types.ModuleType | str | tuple[str],
    *,
    type_filter: type | None | types.UnionType = None,
    module_filter: str | None = None,
    filter_by___all__: bool = False,
    recursive: bool = False,
) -> Iterator[type]:
    """Yield classes from given module.

    Arguments:
        module: either a module or a path to a module in form of str or
                tuple of strings.
        type_filter: only yield classes which are subclasses of given type.
        module_filter: filter by a module prefix.
        filter_by___all__: Whether to filter based on whats defined in __all__.
        recursive: import all submodules recursively and also yield their classes.
    """
    if isinstance(module, str | tuple | list):
        if isinstance(module, tuple | list):
            module = ".".join(module)
        try:
            module = importlib.import_module(module)
        except ImportError:
            logger.warning(f"Could not import {module!r}")
            return []
    if recursive:
        for _name, submod in inspect.getmembers(module, inspect.ismodule):
            if submod.__name__.startswith(module_filter or ""):
                yield from iter_classes_for_module(
                    submod,
                    type_filter=type_filter,
                    module_filter=submod.__name__,
                    filter_by___all__=filter_by___all__,
                    recursive=True,
                )
    for klass_name, kls in inspect.getmembers(module, inspect.isclass):
        has_all = hasattr(module, "__all__")
        if filter_by___all__ and (not has_all or klass_name not in module.__all__):
            continue
        if type_filter is not None and not issubclass(kls, type_filter):
            continue
        if module_filter is not None and not kls.__module__.startswith(module_filter):
            continue
        yield kls


def get_topmost_module_path_for_klass(klass: type) -> str:
    """Return path of topmost module containing given class."""
    path = klass.__module__
    parts = path.split(".")
    while parts:
        with contextlib.suppress(TypeError):
            new_path = ".".join(parts)
            mod = importlib.import_module(new_path)
            klasses = [kls for _kls_name, kls in inspect.getmembers(mod, inspect.isclass)]
            if klass in klasses:
                path = new_path
        parts = parts[:-1]
    return path


if __name__ == "__main__":
    from prettyqt import widgets

    path = iter_classes_for_module(widgets, recursive=False)
    print(len(list(path)))
