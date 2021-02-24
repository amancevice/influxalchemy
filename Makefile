PYFILES := $(shell find influxalchemy tests -name '*.py')
SDIST   := dist/$(shell python setup.py --fullname).tar.gz

all: $(SDIST)

clean:
	rm -rf dist

upload: $(SDIST)
	twine upload $<

.PHONY: all clean upload

$(SDIST): $(PYFILES) Pipfile.lock
	pipenv run pytest
	python setup.py sdist

Pipfile.lock: Pipfile
	pipenv install --dev
