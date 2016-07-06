#!/usr/bin/python3
'''
========
botogram
========

botogram is a Python framework, which allows you to focus just on
creating your `Telegram bots`_, without worrying about the underlying
Bots API.

While most of the libraries for Telegram out there just wrap the Bots
API, botogram focuses heavily on the development experience, aiming to
provide you the best API possible. Most of the Telegram implementation
details are managed by botogram, so you can just focus on your bot.

::

    import botogram
    bot = botogram.create("API-KEY")

    @bot.command("hello")
    def hello_command(chat, message, args):
        """Say hello to the world!"""
        chat.send("Hello world")

    if __name__ == "__main__":
        bot.run()

Want to get started? `Go to the documentation`_

.. _Telegram bots: https://core.telegram.org/bots
.. _Go to the documentation: https://botogram.pietroalbini.io/docs
'''

import setuptools


setuptools.setup(
    name = "botogram",
    version = "0.3.3",
    url = "https://botogram.pietroalbini.io",

    license = "MIT",

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.io",

    description = "A Python framework for Telegram bots",
    long_description = __doc__,

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
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
