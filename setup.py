#!/usr/bin/python3

import setuptools


setuptools.setup(
    name = "botogram",
    version = "1.0.dev0",
    url = "http://botogram.pietroalbini.io",

    license = "MIT",

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.io",

    description = "A Python microframework for Telegram bots",

    packages = [
        "botogram",
        "botogram.objects",
        "botogram.runner",
    ],

    install_requires = [
        "requests",
        "logbook",
    ],

    include_package_data = True,
    zip_safe = False,

    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
