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

generate_linear_regression_model:
	$(PYTHON) scripts/generate_linear_regression_model.py

generate_decision_tree_model:
	$(PYTHON) scripts/generate_decision_tree_model.py

generate_random_forest_model:
	$(PYTHON) scripts/generate_random_forest_model.py

generate_adaboost_model:
	$(PYTHON) scripts/generate_adaboost_model.py

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
