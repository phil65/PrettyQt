# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import uic


def create_ui(source, target):
    if isinstance(source, str):
        source = pathlib.Path(source)
    if isinstance(target, str):
        target = pathlib.Path(target)
    ui_files = [i for i in source.iterdir() if i.suffix == ".ui"]
    for ui_filename in ui_files:
        py_filename = ui_filename.with_suffix(".py")
        with (target / py_filename.name).open(mode="w") as fout:
            uic.compileUi(str(source / ui_filename), fout, from_imports=True)
            print(f"{py_filename.name} created in {target}.")
    # resources_path = target.parent.parent.parent / "resources" / "resources.qrc"
    # resources_output_path = target / "resources_rc.py"
    # os.system(f"pyrcc5.exe -o {resources_output_path} {resources_path}")
    # print(f"created {resources_output_path}.")
    #  pyrcc5.exe -o resources.py .\resources.qrc
