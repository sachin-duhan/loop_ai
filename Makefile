PYTHON=$(shell which python3 )
VERSION=`cat heimdall/VERSION`

ifeq (, $(PYTHON))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.7
PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'from sys import version_info as v; v_min=int("".join("$(PYTHON_VERSION_MIN)".split("."))); print(0) if int(str(v.major)+str(v.minor)) >= v_min else print(1)')
PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )

PIP=$(PYTHON) -m pip
PYDOC=pydoc3

ifeq ($(PYTHON_VERSION_OK),1)
  $(error "Requires Python >= $(PYTHON_VERSION_MIN) - Installed: $(PYTHON_VERSION)")
endif

help: ## Print help for each target
	$(info Things3 low-level Python API.)
	$(info =============================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

.PHONY: run
run: ## Run flask application.
	PYTHONPATH="." $(PYTHON) app/scripts/create_db.py
	PYTHONPATH="." $(PYTHON) app/main.py


.PHONY: load
load: ## Loads file data to db.
	PYTHONPATH="." $(PYTHON) app/scripts/create_db.py

.PHONY: install
install: ## Installs dependencies.
	$(PIP) install -r requirements.txt

.PHONY: clean
clean: ## remove the python binary files.
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	rm -rf build dist *.egg-info .pytest_cache cov_html .coverage

.PHONY: lint
lint: ## Lint the code
	flake8

.PHONY: test
test: dev-install pytest

.PHONY: dev-install
dev-install: ## Install testing in development mode.
	$(PIP) install -r requirements.txt

.PHONY: pytest
pytest: ## Tests the code base and creates code coverage report.
	$(PYTHON) -m pytest

.PHONY: check-black
check-black: ## Formats and checks code quality standards.
	$(PYTHON) -m black --check .
	$(PYTHON) -m black --check tests/

PHONY: check-isort
check-isort:
	$(PYTHON) -m isort --profile black . --check-only
	$(PYTHON) -m isort --profile black tests --check-only

.PHONY: code-analysis
code-analysis: check-black check-isort lint bandit safety

doc: ## Document the code
	@$(PYDOC) .

