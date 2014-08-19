characteristic: Say 'yes' to types but 'no' to typing!
======================================================

Release v\ |release| (:doc:`What's new? <changelog>`).


.. include:: ../README.rst
   :start-after: begin


Teaser
------

.. doctest::

   >>> from characteristic import Attribute, attributes
   >>> @attributes(["a", "b"])
   ... class AClass(object):
   ...     pass
   >>> @attributes(["a", Attribute("b", default_value="abc", instance_of=str)])
   ... class AnotherClass(object):
   ...     pass
   >>> obj1 = AClass(a=1, b="abc")
   >>> obj2 = AnotherClass(a=1, b="abc")
   >>> obj3 = AnotherClass(a=1)
   >>> AnotherClass(a=1, b=42)
   Traceback (most recent call last):
    ...
   TypeError: Attribute 'b' must be an instance of 'str'.
   >>> print obj1, obj2, obj3
   <AClass(a=1, b='abc')> <AnotherClass(a=1, b='abc')> <AnotherClass(a=1, b='abc')>
   >>> obj1 == obj2
   False
   >>> obj2 == obj3
   True


User's Guide
------------

.. toctree::
   :maxdepth: 1

   why
   examples
   api

Project Information
^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   license
   contributing
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

