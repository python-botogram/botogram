.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _install:

========================
Installation of botogram
========================

This tutorial will guide you through botogram's installation process.

.. _install-dependencies:

Getting started
===============

In order to install botogram you will need to manually install some tools that
are used during the build process. Before proceeding please make sure to have
Python_ 3.4 or newer installed, along with the pip_ command line utility.

Installing virtualenv
---------------------

Virtual environments are necessary to create isolated Python installations that
allow you to manage dependencies for different projects. Using pip, installing
the virtualenv_ tool is trivial::

   $ [sudo] python3 -m pip install virtualenv

Please refer to the `virtualenv documentation <install virtualenv>`_ if you wish
to install virtualenv from source.

Installing invoke
-----------------

botogram uses invoke_ for managing tasks. You can think of it like a sort of
Makefile for the project. As for virtualenv, the recommended installation
process uses pip::

   $ python3 -m pip install invoke

More information on the installation process can be found on the
`PyInvoke documentation <install pyinvoke>`_.

Installing from the Python Packages Index
=========================================

botogram releases are available `from the Python Packages Index`_ and can be
installed using pip. This is the recommended way of installing the package and
should work for the majority of usecases::

   $ python3 -m pip install botogram

Perfect, botogram is now installed! Now, you can follow the
":ref:`tutorial`" chapter if you want to create a bot right now!

.. _install-edge:

Living on the edge
==================

If you don't mind having some instability or bugs, and you want the latest
features not yet released, you can clone the `botogram git repository`_, and
execute the installation from source::

   $ git clone https://github.com/pietroalbini/botogram.git
   $ cd botogram
   $ invoke install

Remember that something can change without notice, and even be removed, until
the feature is released, so don't use a non-released version in production.

.. _install-venvs:

About virtual environments
==========================

Installing Python packages globally isn't a good practice. A large part of the
Python community solves this problem with a tool called virtualenv_, which
creates a small, isolated Python installation for each project. This allows
you to experiment in a project without affecting other ones.

We'll assume you've already installed virtualenv as explained above. Next, you
can issue the following command to create a virtual environment in ``env/``::

   $ virtualenv -p python3 env

So, you've now a virtual environment with Python 3 in it. In order to activate
it, you can source into the terminal the ``bin/activate`` script::

   $ source env/bin/activate

Now, everything you install with pip will be confined in that environment.
This means you need to enter the virtual environment every time you want to
run the script. When you're done working in the virtual environment, you can
exit by calling the ``deactivate`` command::

   $ deactivate

.. _install-troubleshooting:

Troubleshooting
===============

You might encounter some errors while installing botogram. Here is explained how
to fix the most recurring ones:

Insufficient permissions
------------------------

On some linux systems, you usually don't have enough privileges to install
something globally. In this case, you can ask your system administrator to
execute the above command, or you can wrap the command with sudo, if you
are allowed to do so::

   $ sudo pip3 install botogram

If you installed from source, you need to use this command instead of the last
one::

   $ sudo invoke install

.. _from the Python Packages Index: https://pypi.python.org/pypi/botogram
.. _pip: https://pip.pypa.io
.. _Python: https://www.python.org
.. _setuptools: https://setuptools.pypa.io
.. _botogram git repository: https://github.com/pietroalbini/botogram
.. _virtualenv: https://virtualenv.pypa.io
.. Apparently pyinvoke's documentation is no longer being served over HTTPS
.. _invoke: http://www.pyinvoke.org
.. _install virtualenv: https://virtualenv.pypa.io/en/latest/installation.html
.. _install pyinvoke: http://www.pyinvoke.org/installing.html
