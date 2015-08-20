# botogram's makefile
#
# Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
# Released under the MIT license

.PHONY: build install devel i18n docs test lint clean


# Package build

build: build/packages/*.tar.gz build/packages/*.whl

build/envs/build: requirements-build.txt
	@rm -rf build/envs/build
	@mkdir -p build/envs/build
	virtualenv -p python3 build/envs/build
	build/envs/build/bin/pip install -r requirements-build.txt

build/packages/*.tar.gz: i18n build/envs/build botogram/** setup.py
	@rm -f build/packages/*.tar.gz
	build/envs/build/bin/python3 setup.py sdist -d build/packages

build/packages/*.whl: i18n build/envs/build botogram/** setup.py
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

botogram.egg-info: i18n build/envs/devel setup.py
	build/envs/devel/bin/pip install -e .
	@touch botogram.egg-info


# Internationalization

i18n: $(subst i18n/langs,botogram/i18n,$(subst .po,.mo,$(wildcard i18n/langs/*.po)))

i18n/botogram.pot: build/envs/build botogram/
	@build/envs/build/bin/pybabel extract botogram -o i18n/botogram.pot \
		-w 79 \
		--msgid-bugs-address=https://github.com/pietroalbini/botogram/issues \
		--copyright-holder="Pietro Albini <pietro@pietroalbini.io>" \
		--project=`python3 setup.py --name` \
		--version=`python3 setup.py --version`

i18n/langs/%.po: build/envs/build i18n/botogram.pot botogram/
	@if [ -f $@ ]; then \
		build/envs/build/bin/pybabel update -i i18n/botogram.pot \
		-o $@ -l `basename $@ .po`; \
	else \
		build/envs/build/bin/pybabel init -i i18n/botogram.pot -o $@ \
		-l `basename $@ .po`; \
	fi

botogram/i18n/%.mo: build/envs/build i18n/langs/%.po
	@mkdir -p botogram/i18n
	@build/envs/build/bin/pybabel compile \
		-i i18n/langs/`basename $@ .mo`.po \
		-o $@ -l `basename $@ .mo`


# Documentation

docs: build/docs

build/envs/docs: requirements-docs.txt
	@rm -rf build/envs/docs
	@mkdir -p build/envs/docs
	virtualenv -p python3 build/envs/docs
	build/envs/docs/bin/pip install -r requirements-docs.txt

build/docs: build/envs/docs docs/**
	@rm -rf build/docs
	build/envs/docs/bin/buildthedocs docs/buildthedocs.yml -o build/docs


# Testing

test: build/envs/test
	@build/envs/test/bin/py.test tests/

build/envs/test: requirements-test.txt
	@rm -rf build/envs/test
	@mkdir -p build/envs/test
	virtualenv -p python3 build/envs/test
	build/envs/test/bin/pip install -r requirements-test.txt
	build/envs/test/bin/pip install -e .


# Lint

lint: build/envs/lint
	@build/envs/lint/bin/flake8 botogram --builtins InterruptedError

build/envs/lint: requirements-lint.txt
	@rm -rf build/envs/lint
	@mkdir -p build/envs/lint
	@virtualenv -p python3 build/envs/lint
	@build/envs/lint/bin/pip install -r requirements-lint.txt


# Cleanup

clean:
	@rm -rf build
	@rm -rf botogram.egg-info
	@rm -f i18n/botogram.pot
	@rm -f botogram/i18n/*.mo


# Help message

help:
	@echo "Available targets:  (default is 'build')"
	@echo "- build       Create the .tar.gz and .whl packages"
	@echo "- install     Install botogram in the current environment"
	@echo "- devel       Setup the development environment"
	@echo "- i18n        Build the language files"
	@echo "- docs        Build the documentation"
	@echo "- clean       Clean up the source directory"
