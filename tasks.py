# Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

# Version check, ensure it's run with Python 3
import sys
import os
if sys.version_info[0] < 3:
    print("Hey! It seems you installed invoke for Python 2!")
    print("Please make sure you installed it with Python 3, else this script "
          "won't work.")
    print("")
    print("In order to fix the issue, please execute the following commands:")
    if os.name == "nt":
        print("  py -m pip uninstall invoke")
        print("  py -3 -m pip install invoke")
    else:
        print("  python -m pip uninstall invoke")
        print("  python3 -m pip install invoke")
    exit(1)

import shutil
import glob
import re

import invoke


# This is because invoke can't keep backward compatibility...
_invoke_v = invoke.__version__.split(".")
if int(_invoke_v[0]) == 0 and int(_invoke_v[1]) <= 12:
    invoke.task = invoke.ctask


BASE = os.path.dirname(__file__)
PYTHON = "python3"
PROJECT = "botogram"
VERSION = "1.0.dev0"

ISSUES = "https://github.com/pietroalbini/botogram/issues"
COPYRIGHT = "Pietro Albini <pietro@pietroalbini.io>"


def create_env(name, requirements=False, self=False, force=False):
    """Create a new virtual environment"""
    path = os.path.join(BASE, "build", "envs", name)

    # Don't re-create the environment if force is False
    if os.path.exists(path):
        if force:
            shutil.rmtree(path)
        else:
            return path

    invoke.run("virtualenv -p %s %s" % (PYTHON, path))
    if requirements:
        invoke.run("%s/bin/pip install -r requirements-%s.txt" % (path, name))
    if self:
        invoke.run("%s/bin/pip install -e ." % path)

    return path


def remove_dir_content(path):
    """Remove the content of a directory"""
    for file in glob.glob(os.path.join(path, "*")):
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)


#
# Cleanup
#


@invoke.task
def clean(ctx):
    """Clean all the build things"""
    for dir in "build", "%s.egg-info" % PROJECT:
        path = os.path.join(BASE, dir)
        if not os.path.exists(path):
            continue
        shutil.rmtree(path)

    exclude = ["%s/.git" % BASE, "%s/build" % BASE]
    remove_files = [re.compile(r'.py[co]$'), re.compile(r'.mo$')]
    remove_dirs = [re.compile('__pycache__')]

    # Remove all the unwanted things
    for root, dirs, files in os.walk(BASE, topdown=False):
        # Skip excluded directories
        skip = False
        for one in exclude:
            if one == root or (root != BASE and one.startswith(root)):
                skip = True
                break
        if skip:
            continue

        # Remove all the unwanted files
        for file in files:
            file = os.path.join(root, file)
            for regex in remove_files:
                if regex.search(file):
                    os.remove(file)

        # Remove all the unwanted directories
        for dir in dirs:
            dir = os.path.join(root, dir)
            for regex in remove_dirs:
                if regex.search(dir):
                    shutil.rmtree(dir)


#
# Internationalization
#


def i18n_available():
    """Return a list of all the available langs"""
    base = os.path.join(BASE, "i18n", "langs")
    for path in glob.glob("%s/*.po" % base):
        yield os.path.basename(path).rsplit(".", 1)[0]


@invoke.task(name="i18n-compile")
def i18n_compile(ctx):
    """Compile the translation files"""
    env = create_env("build", requirements=True)

    dest_dir = os.path.join(BASE, PROJECT, "i18n")
    orig_dir = os.path.join(BASE, "i18n", "langs")
    os.makedirs(dest_dir, exist_ok=True)

    for lang in i18n_available():
        invoke.run("%s/bin/pybabel compile -i %s/%s.po -o %s/%s.mo -l %s" %
                   (env, orig_dir, lang, dest_dir, lang, lang))


@invoke.task(name="i18n-extract")
def i18n_extract(ctx):
    """Extract all the messages from the source code"""
    env = create_env("build", requirements=True)

    base = os.path.join(BASE, "i18n")
    langs_dir = os.path.join(base, "langs")

    invoke.run("%s/bin/pybabel extract %s -o %s/%s.pot -w 79 "
               "--msgid-bugs-address \"%s\" --copyright-holder \"%s\" "
               "--project %s --version %s" %
               (env, PROJECT, base, PROJECT, ISSUES, COPYRIGHT, PROJECT,
                   VERSION))

    for lang in i18n_available():
        invoke.run("%s/bin/pybabel update -i %s/%s.pot -o %s/%s.po -l %s" %
                   (env, base, PROJECT, langs_dir, lang, lang))


@invoke.task(name="i18n-new")
def i18n_new(ctx, lang):
    """Create a new language file"""
    env = create_env("build", requirements=True)

    base = os.path.join(BASE, "i18n")
    langs_dir = os.path.join(base, "langs")

    if lang in i18n_available():
        print("The language \"%s\" already exists" % lang)
        exit(1)

    invoke.run("%s/bin/pybabel init -i %s/%s.pot -o %s/%s.po -l %s" %
               (env, base, PROJECT, langs_dir, lang, lang))


#
# Build and installation
#


@invoke.task
def devel(ctx):
    """Setup the development environment"""
    create_env("devel", self=True, force=True)


@invoke.task(pre=[i18n_compile])
def build(ctx):
    """Create a new build"""
    env = create_env("build", requirements=True)

    out = os.path.join(BASE, "build", "packages")
    if os.path.exists(out):
        remove_dir_content(out)

    for type in "sdist", "bdist_wheel":
        invoke.run("%s/bin/python setup.py %s -d %s" % (env, type, out))


@invoke.task(pre=[build])
def install(ctx):
    """Install the program on this environment"""
    invoke.run("python3 -m pip install --upgrade build/packages/*whl")



#
# Testing
#


@invoke.task
def test(ctx):
    """Run the test suite"""
    env = create_env("test", requirements=True, self=True)

    invoke.run("%s/bin/py.test tests" % env, pty=True)


#
# Linting
#


@invoke.task
def lint(ctx):
    """Lint the source code"""
    FLAKE8_OPTIONS = "--select=E,W,F,C9,N8"
    env = create_env("lint", requirements=True)

    invoke.run("%s/bin/flake8 %s %s" % (env, FLAKE8_OPTIONS, PROJECT))


#
# Documentation
#


@invoke.task
def docs(ctx):
    """Build the documentation"""
    env = create_env("docs", requirements=True)

    docs_dir = os.path.join(BASE, "docs")
    build_dir = os.path.join(BASE, "build", "docs")
    remove_dir_content(build_dir)

    invoke.run("%s/bin/buildthedocs %s/buildthedocs.yml -o %s" %
               (env, docs_dir, build_dir))


#
# Pinned dependencies management
#


@invoke.task(name="deps-sync")
def deps_sync(ctx):
    """Sync dependencies versions"""
    env = create_env("tools", requirements=True)

    for env_name in os.listdir(os.path.join(BASE, "build", "envs")):
        req = os.path.join(BASE, "requirements-%s.txt" % env_name)
        if not os.path.exists(req):
            continue

        sub_env = os.path.join(BASE, "build", "envs", env_name)
        invoke.run("VIRTUAL_ENV=%s %s/bin/pip-sync %s/requirements-%s.txt"
                   % (sub_env, env, BASE, env_name), pty=True)


@invoke.task(name="deps-compile")
def deps_compile(ctx):
    """Compile new requirements-*.txt"""
    env = create_env("tools", requirements=True)

    for file in glob.glob(os.path.join(BASE, "requirements-*.in")):
        invoke.run("%s/bin/pip-compile %s > %s" % (env, os.path.abspath(file),
                   os.path.abspath(file)[:-3] + ".txt"))
