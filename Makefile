PYTHON_MODULES := pyCBPE
PYTHONPATH := .
VENV := venv
BIN := $(VENV)/bin

PYTHON := env PYTHONPATH=$(PYTHONPATH) $(BIN)/python
PIP := $(BIN)/pip

REQUIREMENTS := -r requirements.txt
PRE_COMMIT := $(BIN)/pre-commit

run:
	$(PYTHON) scripts/main.py

tester:
	$(PYTHON) scripts/tester.py

generate_model:
	$(PYTHON) scripts/generate_model.py

bootstrap: venv \
			requirements \

clean:
	rm -r $(VENV)

venv:
	python3 -m venv $(VENV)

requirements:
	$(PIP) install $(REQUIREMENTS)
