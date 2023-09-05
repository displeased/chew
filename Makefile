fmt:
	black chew/
.PHONY: fmt

check:
	pylint chew || true
	mypy chew || true
.PHONY: check

clean:
	find . -type d -name '__pycache__' | xargs rm -rf
	rm -rf .mypy_cache .coverage
.PHONY: clean

distclean: clean
	rm -rf .venv/ dist/ .pdm-python
.PHONY: distclean

test:
	python3 -m unittest discover tests
.PHONY: test

test_check:
	pylint -d missing-function-docstring,wildcard-import,missing-class-docstring,too-many-public-methods,unused-wildcard-import tests
.PHONY: test_check

coverage:
	python3 -m coverage run -m unittest discover tests
	python3 -m coverage report -m
.PHONY: coverage
