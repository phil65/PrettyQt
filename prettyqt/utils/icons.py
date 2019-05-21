# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff

for full list, see:
- https://cdn.materialdesignicons.com/3.0.39/
"""

import qtawesome as qta


class IconProvider(object):
    ICONS: dict = dict()
    WINDOW_ICONS: dict = dict()


def reset_icons():
    IconProvider.ICONS = dict()


def get_icon(name):
    if name not in IconProvider.ICONS:
        IconProvider.ICONS[name] = qta.icon(name)
    return IconProvider.ICONS[name]


def get_window_icon(name):
    if name not in IconProvider.WINDOW_ICONS:
        IconProvider.WINDOW_ICONS[name] = qta.icon(name, color="lightgray")
    return IconProvider.WINDOW_ICONS[name]


def set_defaults(*args, **kwargs):
    qta.set_defaults(*args, **kwargs)
    reset_icons()
