.. _why:

Why?
====

The difference between namedtuple_\ s and classes decorated by ``characteristic`` is that the latter are type-sensitive and less typing aside regular classes:


.. doctest::

   >>> from characteristic import Attribute, attributes
   >>> @attributes([Attribute("a", instance_of=int)])
   ... class C1(object):
   ...     def __init__(self):
   ...         if self.a >= 5:
   ...             raise ValueError("'a' must be smaller 5!")
   ...     def print_a(self):
   ...         print self.a
   >>> @attributes([Attribute("a", instance_of=int)])
   ... class C2(object):
   ...     pass
   >>> c1 = C1(a=1)
   >>> c2 = C2(a=1)
   >>> c1.a == c2.a
   True
   >>> c1 == c2
   False
   >>> c1.print_a()
   1
   >>> C1(a=5)
   Traceback (most recent call last):
      ...
   ValueError: 'a' must be smaller 5!


…while namedtuple’s purpose is *explicitly* to behave like tuples:


.. doctest::

   >>> from collections import namedtuple
   >>> NT1 = namedtuple("NT1", "a")
   >>> NT2 = namedtuple("NT2", "b")
   >>> t1 = NT1._make([1,])
   >>> t2 = NT2._make([1,])
   >>> t1 == t2 == (1,)
   True


This can easily lead to surprising and unintended behaviors.

.. _namedtuple: https://docs.python.org/2/library/collections.html#collections.namedtuple
.. _tuple: https://docs.python.org/2/tutorial/datastructures.html#tuples-and-sequences
