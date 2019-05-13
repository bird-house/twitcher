# Application
APP_ROOT := $(CURDIR)
APP_NAME := twitcher

# Anaconda
CONDA := $(shell command -v conda 2> /dev/null)
ANACONDA_HOME := $(shell conda info --base 2> /dev/null)
CONDA_ENV := $(APP_NAME)

# Temp files
TEMP_FILES := *.egg-info *.log *.sqlite

# end of configuration

.DEFAULT_GOAL := help

.PHONY: all
all: help

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  help        to print this help message. (Default)"
	@echo "  install     to install $(APP_NAME) by running 'python setup.py develop'."
	@echo "  db          to upgrade or initialize database."
	@echo "  start       to start $(APP_NAME) service as daemon (background process)."
	@echo "  clean       to delete all files that are created by running buildout."
	@echo "\nTesting targets:"
	@echo "  test        to run tests (but skip long running tests)."
	@echo "  testall     to run all tests (including long running tests)."
	@echo "  pep8        to run pep8 code style checks."
	@echo "\nSphinx targets:"
	@echo "  docs        to generate HTML documentation with Sphinx."
	@echo "\nDeployment targets:"
	@echo "  spec        to generate Conda spec file."

## Conda targets

.PHONY: check_conda
check_conda:
ifndef CONDA
		$(error "Conda is not available. Please install miniconda: https://conda.io/miniconda.html")
endif

.PHONY: conda_env
conda_env: check_conda
	@echo "Updating conda environment $(CONDA_ENV) ..."
	"$(CONDA)" env update -n $(CONDA_ENV) -f environment.yml

.PHONY: envclean
envclean: check_conda
	@echo "Removing conda env $(CONDA_ENV)"
	@-"$(CONDA)" remove -n $(CONDA_ENV) --yes --all

.PHONY: spec
spec: check_conda
	@echo "Updating conda environment specification file ..."
	@-"$(CONDA)" list -n $(CONDA_ENV) --explicit > spec-file.txt

## Build targets

.PHONY: bootstrap
bootstrap: check_conda conda_env bootstrap_dev
	@echo "Bootstrap ..."

.PHONY: bootstrap_dev
bootstrap_dev:
	@echo "Installing development requirements for tests and docs ..."
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV) && pip install -r requirements_dev.txt"

.PHONY: install
install: bootstrap
	@echo "Installing application ..."
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV) && python setup.py develop"
	@echo "\nStart service with \`make start'"

.PHONY: db
db:
	@echo "Upgrade or initialize database ..."
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV) && alembic -c development.ini upgrade head"
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV) && initialize_twitcher_db development.ini"

.PHONY: start
start: check_conda
	@echo "Starting application ..."
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV) && pserve development.ini &"

.PHONY: clean
clean: srcclean envclean
	@echo "Cleaning generated files ..."
	@-for i in $(TEMP_FILES); do \
  	test -e $$i && rm -v -rf $$i; \
  done

.PHONY: srcclean
srcclean:
	@echo "Removing *.pyc files ..."
	@-find $(APP_ROOT) -type f -name "*.pyc" -print | xargs rm

.PHONY: distclean
distclean: clean
	@echo "Cleaning ..."
	@git diff --quiet HEAD || echo "There are uncommited changes! Not doing 'git clean' ..."
	@-git clean -dfx

## Test targets

.PHONY: test
test: check_conda
	@echo "Running tests (skip slow and online tests) ..."
	@bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV);pytest -v -m 'not slow and not online' tests/"

.PHONY: testall
testall: check_conda
	@echo "Running all tests (including slow and online tests) ..."
	@bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV) && pytest -v tests/"

.PHONY: pep8
pep8: check_conda
	@echo "Running pep8 code style checks ..."
	@bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV) && flake8"

##  Sphinx targets

.PHONY: docs
docs: check_conda
	@echo "Generating docs with Sphinx ..."
	@-bash -c "source $(ANACONDA_HOME)/bin/activate $(CONDA_ENV);$(MAKE) -C $@ clean html"
	@echo "open your browser: open docs/build/html/index.html"
