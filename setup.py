#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import sys
from setuptools import find_packages, setup
from sphinx.setup_command import BuildDoc

with open("README.rst") as readme_file:
    README = readme_file.read()

with open("HISTORY.rst") as history_file:
    HISTORY = history_file.read()

version = '.'.join(map(str, sys.version_info))

REQUIRES_PYTHON = ">=3.6.0"
REQUIREMENTS = ["qtpy", "docutils", "qtawesome", "bidict", "orjson", "regex"]
SETUP_REQUIREMENTS = ["pytest-runner", ]
TEST_REQUIREMENTS = ["pytest", "pytest-xvfb", "pytest-qt"]

if version == '3.6':
    REQUIREMENTS.append("dataclasses")

setup(
    author="Philipp Temminghoff",
    author_email="phil65@kodi.tv",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Pythonic layer on top of PyQt5 / PySide2",
    install_requires=REQUIREMENTS,
    license="MIT license",
    python_requires=REQUIRES_PYTHON,
    long_description=README + "\n\n" + HISTORY,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="prettyqt",
    name="prettyqt",
    packages=find_packages(),
    setup_requires=SETUP_REQUIREMENTS,
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    url="https://github.com/phil65/prettyqt",
    version="0.69.0",
    zip_safe=False,
    cmdclass={"build_sphinx": BuildDoc}
)
