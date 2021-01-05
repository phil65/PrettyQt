# This is a PyInstaller `hook
# <https://pyinstaller.readthedocs.io/en/stable/hooks.html>`_.
# See the `PyInstaller manual <https://pyinstaller.readthedocs.io/>`_
# for more information.
#
from __future__ import annotations

from PyInstaller.utils.hooks import collect_data_files


# For more information see
# `hook global variables
# <https://pyinstaller.readthedocs.io/en/stable/hooks.html#hook-global-variables>`_
# in the manual for more information.

# hiddenimports = ["pyi_hooksample._hidden"]
# The ``excludes`` parameter of `collect_data_files
# <https://pyinstaller.readthedocs.io/en/stable/hooks.html#useful-items-in-pyinstaller-utils-hooks>`_
# excludes ``rthooks.dat`` from the frozen executable, which is only needed when
# freezeing, but not when executing the frozen program.
datas = collect_data_files("prettyqt", excludes=["__pyinstaller"])
