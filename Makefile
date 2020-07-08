.PHONY: help clean lint test docs serve release bump
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys
from urllib.request import pathname2url
webbrowser.open("file:" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define BUMP_SCRIPT
import os, prettyqt
version = prettyqt.__version__
os.system(f'cz changelog --unreleased-version "v{version}"')
endef
export BUMP_SCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: ## remove all build, test, coverage and Python artifacts
	git clean -dfX

lint: ## check style with flake8
	flake8 prettyqt

test: ## run tests quickly with the default Python
	py.test

docs: ## builds the documentation
	mkdocs build

serve: ## run html server watching file changes in realtime
	$(BROWSER) site/index.html
	mkdocs serve

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

# install: clean ## install the package to the active Python's site-packages
# 	python setup.py install

changelog: ## create changelog
	python -c "$$BUMP_SCRIPT"
	mv CHANGELOG.md docs/changelog.md

bump: ## version bump
	poetry run python prettyqt/scripts/bump.py

bump-minor: ## minor version bump
	bump2version minor --allow-dirty --tag
	git push --tags
	git push
	pip install -e .

bump-patch: ## patch version bump
	bump2version patch --allow-dirty --tag
	git push --tags
	git push
	pip install -e .

bump-major: ## major version bump
	bump2version major --allow-dirty --tag
	git push --tags
	git push
	pip install -e .
