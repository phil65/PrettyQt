# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff

for full list, see:
- https://cdn.materialdesignicons.com/3.0.39/
"""

from typing import Union
import pathlib

import qtawesome as qta
from qtpy import QtGui
from prettyqt import gui


IconType = Union[QtGui.QIcon, str, pathlib.Path, None]


def get_icon(icon: IconType, color: str = "black"):
    if icon is None:
        icon = gui.Icon()
    elif isinstance(icon, str):
        if icon.startswith("mdi."):
            icon = qta.icon(icon, color=color)
        else:
            icon = gui.Icon(icon)
    elif isinstance(icon, pathlib.Path):
        icon = gui.Icon(icon)
    return icon


def set_defaults(*args, **kwargs):
    qta.set_defaults(*args, **kwargs)
