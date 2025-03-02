"""debugging package."""

import enum
import importlib
import inspect

from prettyqt import core


def get_all_qt_classes(only_qobjects: bool = False):
    import PySide6

    return [
        i[1]
        for namespace in PySide6._find_all_qt_modules()
        for i in inspect.getmembers(importlib.import_module(f"PySide6.{namespace}"))
        if (isinstance(i[1], type) and not only_qobjects)
        or (isinstance(i[1], type) and issubclass(i[1], core.QObject))
    ]


def get_all_qt_enums():
    all_qt_enums = [
        i[1]
        for Klass in get_all_qt_classes()
        for i in inspect.getmembers(Klass)
        if isinstance(i[1], enum.EnumType)
    ]

    all_qt_enums.extend([
        i[1] for i in inspect.getmembers(core.Qt) if isinstance(i[1], enum.EnumType)
    ])
    return all_qt_enums


def list_all_properties(only_enums: bool = False):
    props = {}
    for klass in get_all_qt_classes(only_qobjects=True):
        metaobj = core.MetaObject(klass.staticMetaObject)
        klass_props = {
            f"{klass.__name__}.{prop.name()}": prop
            for prop in metaobj.get_properties(include_super=False)
        }
        if only_enums:
            klass_props = {
                k: v for k, v in klass_props.items() if v.get_enumerator_type()
            }
        props |= klass_props
    return props


if __name__ == "__main__":
    import pprint

    pprint.pprint(list_all_properties(only_enums=True))
