.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file:" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

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
	flake8 prettyqt tests

test: ## run tests quickly with the default Python
	py.test

coverage: ## check code coverage quickly with the default Python
	coverage run --source prettyqt -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate HTML documentation
	$(MAKE) -C docs build
	$(BROWSER) docs/site/index.html

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

# install: clean ## install the package to the active Python's site-packages
# 	python setup.py install

bump: ## version bump
# 	git stash --include-untracked
	cz bump --changelog --no-verify
# 	git stash apply
# 	git push --tags
# 	git push
# 	pip install -e .

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
