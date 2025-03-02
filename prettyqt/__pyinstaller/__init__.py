from __future__ import annotations

import pathlib


def get_hook_dirs():
    return [str(pathlib.Path(__file__).parent)]
    # return [str(pathlib.Path(__file__).parent)]
