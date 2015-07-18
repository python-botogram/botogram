# botogram's makefile
#
# Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
# Released under the MIT license

.PHONY: build install devel docs clean


# Package build

build: build/packages/*.tar.gz build/packages/*.whl

build/envs/build:
	@rm -rf build/envs/build
	@mkdir -p build/envs/build
	virtualenv -p python3 build/envs/build

build/packages/*.tar.gz: build/envs/build botogram/** setup.py
	@rm -f build/packages/*.tar.gz
	build/envs/build/bin/python3 setup.py sdist -d build/packages

build/packages/*.whl: build/envs/build botogram/** setup.py
	@rm -rf build/packages/*.whl
	build/envs/build/bin/python3 setup.py bdist_wheel -d build/packages


# Installation

install: build/packages/*.whl
	python3 -m pip install --upgrade build/packages/*.whl


# Development tools

devel: botogram.egg-info

build/envs/devel:
	@rm -rf build/envs/devel
	@mkdir -p build/envs/devel
	virtualenv -p python3 build/envs/devel

botogram.egg-info: build/envs/devel setup.py
	build/envs/devel/bin/pip install -e .
	@touch botogram.egg-info


# Documentation

docs: build/docs

build/envs/docs:
	@rm -rf build/envs/docs
	@mkdir -p build/envs/docs
	virtualenv -p python3 build/envs/docs
	build/envs/docs/bin/pip install -r requirements-docs.txt

build/docs: build/envs/docs docs/**
	@rm -rf build/docs
	build/envs/docs/bin/buildthedocs docs/buildthedocs.yml -o build/docs


# Cleanup

clean:
	@rm -rf build
	@rm -rf botogram.egg-info


# Help message

help:
	@echo "Available targets:  (default is 'build')"
	@echo "- build       Create the .tar.gz and .whl packages"
	@echo "- install     Install botogram in the current environment"
	@echo "- devel       Setup the development environment"
	@echo "- docs        Build the documentation"
	@echo "- clean       Clean up the source directory"
