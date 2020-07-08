# -*- coding: utf-8 -*-
"""
"""

import os
import toml
import pathlib
import subprocess

text = subprocess.check_output("git stash")
stashed = text != b"No local changes to save\n"
print(text, stashed)
os.system("cz bump --no-verify")
dct = toml.load("pyproject.toml")
version = dct["tool"]["poetry"]["version"]
print(version)
os.system(f'cz changelog --unreleased-version "v{version}"')
changelog_file = pathlib.Path("CHANGELOG.md")
text = changelog_file.read_text()
text = text.replace("'", "")
changelog_file.write_text(text)
os.system("cp CHANGELOG.md docs/changelog.md")
os.system("git add --all")
os.system("git commit --amend --no-edit --no-verify")
os.system(f"git tag -d v{version}")
os.system(f"git tag v{version}")
if stashed:
    os.system("git stash apply")
