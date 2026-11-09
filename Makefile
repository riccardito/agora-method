PYTHON ?= python

.PHONY: install demo check test lint all

install:
	$(PYTHON) -m pip install -q -e ".[dev]"

demo:
	$(PYTHON) examples/demo.py

check:
	$(PYTHON) -m agora_checks all

test:
	$(PYTHON) -m pytest --cov --cov-report=term-missing:skip-covered

lint:
	$(PYTHON) -m ruff check .

all: lint check test demo
