.PHONY: install install-dev test test-all flake8 distclean

install:
	python setup.py install

install-dev:
	pip install -q -e .[dev]

test: install-dev
	pytest

test-all: install-dev
	tox

flake8: install-dev
	flake8 freud tests

distclean:
	rm -fr *.egg *.egg-info/ dist/ build/

publish:
	python setup.py sdist bdist_wheel
	twine upload dist/*
	distclean
