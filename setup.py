#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import sys
import pathlib
from setuptools import find_packages, setup

README = pathlib.Path("docs/index.md").read_text()
HISTORY = pathlib.Path("CHANGELOG.md").read_text()

REQUIREMENTS = ["qtpy", "docutils", "qtawesome", "bidict", "orjson", "regex"]
version = ".".join(map(str, sys.version_info))
if version == "3.6":
    REQUIREMENTS.append("dataclasses")
if sys.platform == "darwin":
    REQUIREMENTS.append("darkdetect")

setup(
    author="Philipp Temminghoff",
    author_email="phil65@kodi.tv",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Pythonic layer on top of PyQt5 / PySide2",
    install_requires=REQUIREMENTS,
    license="MIT license",
    python_requires=">=3.6.0",
    long_description=README + "\n\n" + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="prettyqt",
    name="prettyqt",
    packages=find_packages(),
    test_suite="tests",
    url="https://github.com/phil65/prettyqt",
    version="0.84.0",
    zip_safe=False,
)
