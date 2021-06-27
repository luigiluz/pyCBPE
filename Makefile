PYTHON_MODULES := pyCBPE
PYTHONPATH := .
VENV := venv
BIN := $(VENV)/bin

PYTHON := env PYTHONPATH=$(PYTHONPATH) $(BIN)/python
PIP := $(BIN)/pip

REQUIREMENTS := -r requirements.txt
PRE_COMMIT := $(BIN)/pre-commit

generate_dataset:
	$(PYTHON) scripts/generate_dataset.py

plot_key_points:
	$(PYTHON) scripts/plot_key_points.py

generate_model:
	$(PYTHON) scripts/generate_model.py

lib:
	$(PYTHON) -m build

bootstrap: venv \
			requirements \

clean:
	rm -r $(VENV)

venv:
	python3 -m venv $(VENV)

requirements:
	$(PIP) install $(REQUIREMENTS)
