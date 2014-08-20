characteristic: Python attributes without boilerplate.
======================================================

.. image:: https://pypip.in/version/characteristic/badge.svg
   :target: https://pypi.python.org/pypi/characteristic/
   :alt: Latest Version

.. image:: https://travis-ci.org/hynek/characteristic.svg
   :target: https://travis-ci.org/hynek/characteristic
   :alt: CI status

.. image:: https://coveralls.io/repos/hynek/characteristic/badge.png?branch=master
   :target: https://coveralls.io/r/hynek/characteristic?branch=master
   :alt: Current coverage

.. begin


``characteristic`` is an `MIT <http://choosealicense.com/licenses/mit/>`_-licensed Python package with class decorators that ease the chores of implementing the most common attribute-related object protocols.

You just specify the attributes to work with and ``characteristic`` gives you any or all of:

- a nice human-readable ``__repr__``,
- a complete set of comparison methods,
- immutability for attributes,
- and a kwargs-based initializer (that cooperates with your existing one and optionally even checks the types of the arguments)

*without* writing dull boilerplate code again and again.

This gives you the power to use actual classes with actual types in your code instead of confusing ``tuple``\ s or confusingly behaving ``namedtuple``\ s.

So put down that type-less data structures and welcome some class into your life!

``characteristic``\ ’s documentation lives at `Read the Docs <https://characteristic.readthedocs.org/>`_, the code on `GitHub <https://github.com/hynek/characteristic>`_.
It’s rigorously tested on Python 2.6, 2.7, 3.3+, and PyPy.
