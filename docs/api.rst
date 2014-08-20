.. _api:

API
===

.. currentmodule:: characteristic

``characteristic`` consists of several class decorators that add features to your classes.
There are four that add *one* feature each to your class.
And then there's the helper ``@attributes`` that combines them all into one decorator so you don't have to repeat the attribute list multiple times.

Generally the decorators take a list of attributes as their first positional argument.
This list can consists of either native strings\ [*]_ for simple cases or instances of :class:`Attribute` that allow for more customization of ``characteristic``\ 's behavior.

The easiest way to get started is to have a look at the :doc:`examples` to get a feeling for ``characteristic`` and return later for details!

.. [*] Byte strings on Python 2 and Unicode strings on Python 3.


.. note::

   Every argument except for ``attrs`` for decorators and ``name`` for :class:`Attribute` is a **keyword argument**.
   Their positions are coincidental and not guaranteed to remain stable.


.. autofunction:: attributes


.. autofunction:: with_repr

   .. doctest::

      >>> from characteristic import with_repr
      >>> @with_repr(["a", "b"])
      ... class RClass(object):
      ...     def __init__(self, a, b):
      ...         self.a = a
      ...         self.b = b
      >>> c = RClass(42, "abc")
      >>> print c
      <RClass(a=42, b='abc')>


.. autofunction:: with_cmp

   .. doctest::

      >>> from characteristic import with_cmp
      >>> @with_cmp(["a", "b"])
      ... class CClass(object):
      ...     def __init__(self, a, b):
      ...         self.a = a
      ...         self.b = b
      >>> o1 = CClass(1, "abc")
      >>> o2 = CClass(1, "abc")
      >>> o1 == o2  # o1.a == o2.a and o1.b == o2.b
      True
      >>> o1.c = 23
      >>> o2.c = 42
      >>> o1 == o2  # attributes that are not passed to with_cmp are ignored
      True
      >>> o3 = CClass(2, "abc")
      >>> o1 < o3  # because 1 < 2
      True
      >>> o4 = CClass(1, "bca")
      >>> o1 < o4  # o1.a == o4.a, but o1.b < o4.b
      True


.. autofunction:: with_init

   .. doctest::

      >>> from characteristic import with_init, Attribute
      >>> @with_init(["a",
      ...             Attribute("b", default_factory=lambda: 2),
      ...             Attribute("_c")])
      ... class IClass(object):
      ...     def __init__(self):
      ...         if self.b != 2:
      ...             raise ValueError("'b' must be 2!")
      >>> o1 = IClass(a=1, b=2, c=3)
      >>> o2 = IClass(a=1, c=3)
      >>> o1._c
      3
      >>> o1.a == o2.a
      True
      >>> o1.b == o2.b
      True
      >>> IClass()
      Traceback (most recent call last):
        ...
      ValueError: Missing keyword value for 'a'.
      >>> IClass(a=1, b=3)  # the custom __init__ is called after the attributes are initialized
      Traceback (most recent call last):
        ...
      ValueError: 'b' must be 2!

   .. note::

      The generated initializer explicitly does *not* support positional arguments.
      Those are *always* passed to the existing ``__init__`` unaltered.
      Used keyword arguments will *not* be passed to the original ``__init__`` method and have to be accessed on the class (i.e. ``self.a``).


.. autofunction:: immutable

   .. doctest::

      >>> from characteristic import immutable
      >>> @immutable([Attribute("foo")])
      ... class ImmutableClass(object):
      ...     foo = "bar"
      >>> ic = ImmutableClass()
      >>> ic.foo
      'bar'
      >>> ic.foo = "not bar"
      Traceback (most recent call last):
        ...
      AttributeError: Attribute 'foo' of class 'ImmutableClass' is immutable.


   Please note, that that doesn't mean that the attributes themselves are immutable too:

   .. doctest::

      >>> @immutable(["foo"])
      ... class C(object):
      ...     foo = []
      >>> i = C()
      >>> i.foo = [42]
      Traceback (most recent call last):
       ...
      AttributeError: Attribute 'foo' of class 'C' is immutable.
      >>> i.foo.append(42)
      >>> i.foo
      [42]


.. autoclass:: Attribute

.. autofunction:: strip_leading_underscores

   .. doctest::

      >>> from characteristic import strip_leading_underscores
      >>> strip_leading_underscores("_foo")
      'foo'
      >>> strip_leading_underscores("__bar")
      'bar'
      >>> strip_leading_underscores("___qux")
      'qux'

.. autodata:: NOTHING
