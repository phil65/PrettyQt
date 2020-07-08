# -*- coding: utf-8 -*-
"""
"""
import warnings
import functools
import sys


def string_to_num_array(array: str) -> list:
    floats = [float(i) for i in array.split(",")]
    return [int(i) if i.is_integer() else i for i in floats]


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


def is_dark_mode() -> bool:
    if sys.platform.startswith("win"):
        import winreg

        REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        try:
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ
            )
            value, regtype = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
            winreg.CloseKey(registry_key)
            return value == 0
        except WindowsError:
            return False
    elif sys.platform == "darwin":
        import darkdetect

        return darkdetect.isDark()
    else:
        return False
