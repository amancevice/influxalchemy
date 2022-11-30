all: test build

build: .venv
	pipenv run flit build

clean:
	rm -rf dist

ipython:
	pipenv run ipython

publish: test build
	git diff HEAD --quiet
	pipenv run flit publish

test: .venv
	pipenv run black --check influxalchemy tests
	pipenv run pytest

.PHONY: all build clean ipython publish test

Pipfile.lock .venv: Pipfile
	mkdir -p .venv
	pipenv install --dev
	touch .venv
