# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff

for full list, see:
- https://cdn.materialdesignicons.com/3.0.39/
"""

import qtawesome as qta
from prettyqt import gui


def get_icon(icon):
    if not icon:
        icon = gui.Icon()
    elif isinstance(icon, str):
        icon = qta.icon(icon)
    return icon


def set_defaults(*args, **kwargs):
    qta.set_defaults(*args, **kwargs)
