.. _examples:

Examples
========

:func:`@attributes <characteristic.attributes>` together with the definition of the attributes using class attributes enhances your class by:

- a nice ``__repr__``,
- comparison methods that compare instances as if they were tuples of their attributes,
- and -- optionally but by default -- an initializer that uses the keyword arguments to initialize the specified attributes before running the class’ own initializer (you just write the validator!).


.. doctest::

   >>> from characteristic import Attribute, attributes
   >>> @attributes(["a", "b"])
   ... class C(object):
   ...     pass
   >>> obj1 = C(a=1, b="abc")
   >>> obj1
   <C(a=1, b='abc')>
   >>> obj2 = C(a=2, b="abc")
   >>> obj1 == obj2
   False
   >>> obj1 < obj2
   True
   >>> obj3 = C(a=1, b="bca")
   >>> obj3 > obj1
   True

To offer more power and possibilities, a distinct class :class:`Attribute` has been added.
It allows for things like default values for certain attributes, making them optional when ``characteristic``\ 's generated initializer is used:

.. doctest::

   >>> @attributes(["a", "b", Attribute("c", default_value=42)])
   ... class CWithDefaults(object):
   ...     pass
   >>> obj4 = CWithDefaults(a=1, b=2)
   >>> obj5 = CWithDefaults(a=1, b=2, c=42)
   >>> obj4 == obj5
   True

``characteristic`` also offers factories for default values of complex types:

.. doctest::

   >>> @attributes([Attribute("a", default_factory=list),
   ...              Attribute("b", default_factory=dict)])
   ... class CWithDefaultFactory(object):
   ...     pass
   >>> obj6 = CWithDefaultFactory()
   >>> obj6
   <CWithDefaultFactory(a=[], b={})>
   >>> obj7 = CWithDefaultFactory()
   >>> obj7
   <CWithDefaultFactory(a=[], b={})>
   >>> obj6 == obj7
   True
   >>> obj6.a is obj7.a
   False
   >>> obj6.b is obj7.b
   False

Immutable data structures are amazing!
Guess what ``characteristic`` supports?

.. doctest::

   >>> @attributes([Attribute("a")], make_immutable=True)
   ... class ImmutableClass(object):
   ...     pass
   >>> ic = ImmutableClass(a=42)
   >>> ic.a
   42
   >>> ic.a = 43
   Traceback (most recent call last):
    ...
   TypeError: Attribute 'a' of class 'ImmutableClass' is immutable.
   >>> @attributes([Attribute("a")], make_immutable=True)
   ... class AnotherImmutableClass(object):
   ...     def __init__(self):
   ...         self.a *= 2
   >>> ic2 = AnotherImmutableClass(a=21)
   >>> ic2.a
   42
   >>> ic.a = 43
   Traceback (most recent call last):
    ...
   TypeError: Attribute 'a' of class 'AnotherImmutableClass' is immutable.
