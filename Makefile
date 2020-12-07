PYTHON_MODULES := cbpe-python
PYTHONPATH := .
VENV := venv
BIN := $(VENV)/bin

PYTHON := env PYTHONPATH=$(PYTHONPATH) $(BIN)/python
PIP := $(BIN)/pip

REQUIREMENTS := -r requirements.txt
PRE_COMMIT := $(BIN)/pre-commit

bootstrap: venv \
			requirements \

venv:
	python3 -m venv $(VENV)

requirements:
	$(PIP) install $(REQUIREMENTS)