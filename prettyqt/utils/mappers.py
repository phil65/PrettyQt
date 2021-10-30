from __future__ import annotations

from typing import Any

from bidict import bidict

from prettyqt import qt


class FlagMap:
    def __init__(self, initializer, **kwargs):
        self.initializer = initializer
        kwargs = {k: qt.flag_to_int(v) for k, v in kwargs.items()}
        self.bidict: bidict[str, int] = bidict(**kwargs)

        class Inverter:
            def __getitem__(self2, value):
                return self.bidict.inverse[qt.flag_to_int(value)]

        self.inverse = Inverter()

    def __getitem__(self, index):
        return self.initializer(self.bidict[index])

    def __contains__(self, other):
        return other in self.bidict

    def __iter__(self):
        return iter(self.bidict.keys())

    def __getattr__(self, attr):
        return getattr(self.bidict, attr)

    def get_list(self, flag) -> list[Any]:
        flag = int(flag)
        return [k for k, v in self.bidict.items() if v & flag]
