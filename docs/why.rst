.. _why:

Why…
====


…not tuples?
------------


Readability
^^^^^^^^^^^

What does make more sense while debugging::

   <Point(x=1, x=2)>

or::

   (1, 2)

?

Let's add even more ambiguity::

   <Customer(id=42, reseller=23, first_name="Jane", last_name="John")>

or::

   (42, 23, "Jane", "John")

?

Why would you want to write ``customer[2]`` instead of ``customer.first_name``?

Don't get me started when you add nesting.
If you've never ran into mysterious tuples you had no idea what the hell they meant while debugging, you're much smarter then I am.

Using proper classes with names and types makes program code much more readable and comprehensible_.
Especially when trying to grok a new piece of software or returning to old code after several months.

.. _comprehensible: http://arxiv.org/pdf/1304.5257.pdf


Extendability
^^^^^^^^^^^^^

Imagine you have a function that takes or returns a tuple.
Especially if you use tuple unpacking (eg. ``x, y = get_point()``), adding additional data means that you have to change the invocation of that function *everywhere*.

Adding an attribute to a class concerns only those who actually care about that attribute.


…not namedtuples?
-----------------

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

Other than that, ``characteristic`` also adds nifty features like type checks or default values.

.. _namedtuple: https://docs.python.org/2/library/collections.html#collections.namedtuple
.. _tuple: https://docs.python.org/2/tutorial/datastructures.html#tuples-and-sequences
