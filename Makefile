# Project
name    := $(shell python setup.py --name)
runtime := $(shell python -V 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
release := $(shell git describe --tags)
build   := $(name)-$(release)

# Docker Build
image := amancevice/$(name)
digest = $(shell cat build/$(build).build)

dist/$(build).tar.gz: | dist Pipfile.lock .coverage
	docker run --rm $(digest) cat $@ > $@

dist:
	mkdir -p $@

Pipfile.lock: Pipfile | .coverage
	docker run --rm $(digest) cat $@ > $@

.coverage: | build/$(build).build
	docker run --rm $(digest) cat $@ > $@

build/$(build).build: | build
	docker image build \
	--build-arg RUNTIME=$(runtime) \
	--build-arg SETUPTOOLS_SCM_PRETEND_VERSION=$(release) \
	--tag $(image):$(release) .
	docker image inspect --format '{{.Id}}' $(image):$(release) > $@

build:
	mkdir -p $@

.PHONY: shell clean

shell: build/$(build).build
	docker run --rm -it \
	--volume $$PWD:/var/task \
	$(digest) /bin/bash

clean:
	docker image rm -f $(image) $(shell [ -d build ] && cat build/*)
	rm -rf build dist .coverage
