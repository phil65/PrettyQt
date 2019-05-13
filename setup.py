#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup
from sphinx.setup_command import BuildDoc

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["qtpy", "Markdown", "docutils", "qtawesome", "bidict"]

setup_requirements = ["pytest-runner", ]

test_requirements = ["pytest", "pytest-xvfb", "pytest-qt"]

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
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="prettyqt",
    name="prettyqt",
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/phil65/prettyqt",
    version="0.29.0",
    zip_safe=False,
    cmdclass={"build_sphinx": BuildDoc}
)
