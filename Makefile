# Configuration
VERSION := 0.10.1
APP_ROOT := $(abspath $(lastword $(MAKEFILE_LIST))/..)
INI_FILE ?= development.ini

DOCKER_TAG := birdhouse/twitcher:v$(VERSION)
DOCKER_TEST := smoke-test-twitcher
DOCKER_BUILD_XARGS ?=

# Bumpversion 'dry' config
# if 'dry' is specified as target, any bumpversion call using 'BUMP_XARGS' will not apply changes
BUMP_XARGS ?= --verbose --allow-dirty
ifeq ($(filter dry, $(MAKECMDGOALS)), dry)
	BUMP_XARGS := $(BUMP_XARGS) --dry-run
endif
.PHONY: dry
dry: setup.cfg
	@-echo > /dev/null

# end of configuration

.DEFAULT_GOAL := help

.PHONY: all
all: help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  help              to print this help message. (Default)"
	@echo "  install           to install app by running 'pip install -e .'"
	@echo "  develop           to install with additional development requirements."
	@echo "  migrate           to upgrade or initialize database."
	@echo "  start             to start service with 'pserve'."
	@echo "  clean             to remove all files generated by build and tests."
	@echo "\nDocker targets:"
	@echo "  docker-build      to build the docker image with current code base and version."
	@echo "  docker-push       to push the built docker image to the tagged repository."
	@echo "\nTesting targets:"
	@echo "  test              to run tests (but skip long running tests)."
	@echo "  test-local        to run only local tests (skip online tests)."
	@echo "  test-docker       to run smoke test of docker build and execution."
	@echo "  test-all          to run all tests (including long running tests)."
	@echo "  lint              to run code style checks with flake8."
	@echo "  coverage          to generate an HTML report from tests coverage analysis."
	@echo "\nSphinx targets:"
	@echo "  docs              to generate HTML documentation with Sphinx."
	@echo "\nDeployment targets:"
	@echo "  debug             to print variable values employed by this Makefile."
	@echo "  bump              to update the package version."
	@echo "  dry               to only display results (not applied) when combined with 'bump'."
	@echo "  dist              to build source and wheel package."
	@echo "\nSecurity targets:"
	@echo "  gensecret         to generate a secret hash key."
	@echo "  gencert           to generate a self-signed certificate."

.PHONY: debug
debug:
	@-echo "Following variables are used:"
	@-echo "  SHELL:                         $(SHELL)"
	@-echo "  APP_ROOT:                      $(APP_ROOT)"
	@-echo "  VERSION:                       $(VERSION)"
	@-echo "  BUMP_XARGS:                    $(BUMP_XARGS)"
	@-echo "  DOCKER_TAG:                    $(DOCKER_TAG)"

## Build targets

.PHONY: install
install:
	@echo "Installing application ..."
	@-bash -c 'pip install -e .'
	@echo "\nStart service with \`make start'"

.PHONY: develop
develop:
	@echo "Installing development requirements for tests and docs ..."
	@-bash -c 'pip install -e ".[dev]"'

.PHONY: migrate
migrate:
	@echo "Upgrade or initialize database ..."
	@-bash -c 'alembic -c "$(INI_FILE)" upgrade head'
	@-bash -c 'initialize_twitcher_db "$(INI_FILE)"'

.PHONY: start
start:
	@echo "Starting application ..."
	@-bash -c 'pserve "$(INI_FILE)" --reload'

.PHONY: clean
clean: clean-build clean-pyc clean-test

.PHONY: clean-build
clean-build:
	@echo "Remove build artifacts ..."
	@-rm -fr build/
	@-rm -fr dist/
	@-rm -fr .eggs/
	@-find . -name '*.log' -exec rm -fr {} +
	@-find . -name '*.sqlite' -exec rm -fr {} +
	@-find . -name '*.egg-info' -exec rm -fr {} +
	@-find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc:
	@echo "Remove Python file artifacts ..."
	@-find . -name '*.pyc' -exec rm -f {} +
	@-find . -name '*.pyo' -exec rm -f {} +
	@-find . -name '*~' -exec rm -f {} +
	@-find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test:
	@echo "Remove test and coverage artifacts ..."
	@-rm -f .coverage
	@-rm -fr ./coverage/
	@-rm -fr .pytest_cache

.PHONY: clean-dist
clean-dist: clean
	@echo "Run 'git clean' ..."
	@git diff --quiet HEAD || echo "There are uncommited changes! Not doing 'git clean' ..."
	@-git clean -dfx

## Docker targets

.PHONY: docker-build
docker-build:
	@echo "Building docker image: $(DOCKER_TAG)"
	@docker build $(DOCKER_BUILD_XARGS) "$(APP_ROOT)" -t "$(DOCKER_TAG)"

.PHONY: docker-push
docker-push:
	@echo "Pushing docker image: $(DOCKER_TAG)"
	@docker push "$(DOCKER_TAG)"

.PHONY: docker-stop
docker-stop:
	@echo "Stopping test docker container: $(DOCKER_TEST)"
	@-docker container stop "$(DOCKER_TEST)" 2>/dev/null || true
	@-docker rm $(DOCKER_TEST) 2>/dev/null || true

.PHONY: docker-test
docker-test: docker-build docker-stop
	@echo "Smoke test of docker image: $(DOCKER_TAG)"
	docker run --pull never --name $(DOCKER_TEST) -p 8000:8000 -d $(DOCKER_TAG)
	@sleep 2
	@echo "Testing docker image..."
	@(curl http://localhost:8000 | grep "Twitcher Frontpage" && \
	  $(MAKE) docker-stop --no-print-directory || \
 	 ($(MAKE) docker-stop --no-print-directory && \
 	  echo "Failed to obtain expected response from twitcher docker"; exit 1 ))

## Test targets

.PHONY: test
test:
	@echo "Running tests (skip slow and online tests) ..."
	@bash -c 'pytest -v -m "not slow and not online" tests/'

.PHONY: test-local
test-local:
	@echo "Running tests (skip slow and online tests) ..."
	@bash -c 'pytest -v -m "not online" tests/'

.PHONY: test-all
test-all:
	@echo "Running all tests (including slow and online tests) ..."
	@bash -c 'pytest -v tests/'

.PHONY: lint
lint:
	@echo "Running flake8 code style checks ..."
	@bash -c 'flake8'

# run coverage only if .coverage doesn't already exist.
# all other coverage targets will use existing results if available.
.coverage:
	@echo "Running coverage analysis..."
	@bash -c 'pytest --cov -v -m "not slow and not online" tests/'

.PHONY: coverage
coverage: .coverage
	@bash -c 'coverage report -m'
	@bash -c 'coverage html -d coverage'
	@bash -c 'coverage xml -i -o coverage/coverage.xml'
	@-echo "Coverage report: open file://$(APP_ROOT)/coverage/index.html"

## Sphinx targets

.PHONY: docs
docs:
	@echo "Generating docs with Sphinx ..."
	@-bash -c '$(MAKE) -C $@ clean html'
	@echo "open your browser: open file://$(APP_ROOT)/docs/build/html/index.html"

## Deployment targets

.PHONY: bump
bump:
	@-echo "Updating package version ..."
	@[ "${VERSION}" ] || ( echo ">> 'VERSION' is not set"; exit 1 )
	@-bash -c 'bump2version $(BUMP_XARGS) --new-version "${VERSION}" patch;'

.PHONY: dist
dist: clean
	@echo "Builds source and wheel package ..."
	@-python setup.py sdist
	@-python setup.py bdist_wheel
	@ls -l dist

## Security

.PHONY: gensecret
gensecret:
	@echo "Generate a secret ..."
	@-python -c 'import uuid; print(uuid.uuid4().hex)'

.PHONY: gencert
gencert:
	@echo "Generate a self-signed certificate ..."
	@-bash -c "openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem"
	@-bash -c "openssl x509 -pubkey -noout -in cert.pem > pubkey.pem"
