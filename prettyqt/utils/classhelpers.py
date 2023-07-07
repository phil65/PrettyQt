from __future__ import annotations

import collections
import functools
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


def get_subclasses(klass: type, include_abstract: bool = False) -> type:
    for i in klass.__subclasses__():
        yield from get_subclasses(i)
        if include_abstract or not inspect.isabstract(i):
            yield i


def get_class_for_id(base_class: T, id_: str) -> T:
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


def get_module_classes(module: types.ModuleType) -> list[type]:
    clsmembers = inspect.getmembers(module, inspect.isclass)
    return [tpl[1] for tpl in clsmembers]