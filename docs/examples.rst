.. _examples:

Examples
========

:func:`@attributes <characteristic.attributes>` together with the definition of the attributes using class attributes enhances your class by:

- a nice ``__repr__``,
- comparison methods that compare instances as if they were tuples of their attributes,
- and an initializer that uses the keyword arguments to initialize the specified attributes before running the class' own initializer (you just write the validator if you need anything more than type checks!).


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

To offer more power and possibilities, ``characteristic`` comes with a distinct class to define attributes: :class:`~characteristic.Attribute`.
It allows for things like default values for certain attributes, making them optional when ``characteristic``\ 's generated initializer is used:

.. doctest::

   >>> @attributes(["a", "b", Attribute("c", default_value=42)])
   ... class CWithDefaults(object):
   ...     pass
   >>> obj4 = CWithDefaults(a=1, b=2)
   >>> obj4.characteristic_attributes
   [<Attribute(name='a', exclude_from_cmp=False, exclude_from_init=False, exclude_from_repr=False, exclude_from_immutable=False, default_value=NOTHING, default_factory=None, instance_of=None, init_aliaser=None)>, <Attribute(name='b', exclude_from_cmp=False, exclude_from_init=False, exclude_from_repr=False, exclude_from_immutable=False, default_value=NOTHING, default_factory=None, instance_of=None, init_aliaser=None)>, <Attribute(name='c', exclude_from_cmp=False, exclude_from_init=False, exclude_from_repr=False, exclude_from_immutable=False, default_value=42, default_factory=None, instance_of=None, init_aliaser=<function strip_leading_underscores at ...>)>]
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

You can also exclude certain attributes from certain decorators:

.. doctest::

   >>> @attributes(["host", "user",
   ...              Attribute("password", exclude_from_repr=True),
   ...              Attribute("_connection", exclude_from_init=True)])
   ... class DB(object):
   ...     _connection = None
   ...     def connect(self):
   ...         self._connection = "not really a connection"
   >>> db = DB(host="localhost", user="dba", password="secret")
   >>> db.connect()
   >>> db
   <DB(host='localhost', user='dba', _connection='not really a connection')>

Immutable data structures are amazing!
Guess what ``characteristic`` supports?

.. doctest::

   >>> @attributes([Attribute("a")], apply_immutable=True)
   ... class ImmutableClass(object):
   ...     pass
   >>> ic = ImmutableClass(a=42)
   >>> ic.a
   42
   >>> ic.a = 43
   Traceback (most recent call last):
    ...
   AttributeError: Attribute 'a' of class 'ImmutableClass' is immutable.
   >>> @attributes([Attribute("a")], apply_immutable=True)
   ... class AnotherImmutableClass(object):
   ...     def __init__(self):
   ...         self.a *= 2
   >>> ic2 = AnotherImmutableClass(a=21)
   >>> ic2.a
   42
   >>> ic.a = 43
   Traceback (most recent call last):
    ...
   AttributeError: Attribute 'a' of class 'AnotherImmutableClass' is immutable.

You know what else is amazing?
Type checks!

.. doctest::

   >>> @attributes([Attribute("a", instance_of=int)])
   ... class TypeCheckedClass(object):
   ...     pass
   >>> TypeCheckedClass(a="totally not an int")
   Traceback (most recent call last):
    ...
   TypeError: Attribute 'a' must be an instance of 'int'.


And if you want your classes to have certain attributes private, ``characteristic`` will keep your keyword arguments clean if not told otherwise\ [*]_:

.. doctest::

   >>> @attributes([Attribute("_private")])
   ... class CWithPrivateAttribute(object):
   ...     pass
   >>> obj8 = CWithPrivateAttribute(private=42)
   >>> obj8._private
   42
   >>> @attributes([Attribute("_private", init_aliaser=None)])
   ... class CWithPrivateAttributeNoAliasing(object):
   ...     pass
   >>> obj9 = CWithPrivateAttributeNoAliasing(_private=42)
   >>> obj9._private
   42

.. [*] This works *only* for attributes defined using the :class:`~characteristic.Attribute` class.
