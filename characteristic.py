from __future__ import absolute_import, division, print_function

"""
Python attributes without boilerplate.
"""


__version__ = "14.0.0dev"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2014 Hynek Schlawack"


NOTHING = object()


class Attribute(object):
    """
    An attribute that gets defined on classes decorated with
    :func:`attributes`.
    """
    counter = 0  # to be able to order the attributes correctly

    def __init__(self, default=NOTHING):
        self.default = default
        Attribute.counter += 1
        self.counter = Attribute.counter


def with_cmp(attrs):
    """
    A class decorator that adds comparison methods based on *attrs*.

    For that, each class is treated like a ``tuple`` of the values of *attrs*.

    :param attrs: Attributes to work with.
    :type attrs: ``list`` of native strings
    """
    def attrs_to_tuple(obj):
        """
        Create a tuple of all values of *obj*'s *attrs*.
        """
        return tuple(getattr(obj, a) for a in attrs)

    def eq(self, other):
        """
        Automatically created by characteristic.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) == attrs_to_tuple(other)
        else:
            return NotImplemented

    def ne(self, other):
        """
        Automatically created by characteristic.
        """
        result = eq(self, other)
        if result is NotImplemented:
            return NotImplemented
        else:
            return not result

    def lt(self, other):
        """
        Automatically created by characteristic.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) < attrs_to_tuple(other)
        else:
            return NotImplemented

    def le(self, other):
        """
        Automatically created by characteristic.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) <= attrs_to_tuple(other)
        else:
            return NotImplemented

    def gt(self, other):
        """
        Automatically created by characteristic.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) > attrs_to_tuple(other)
        else:
            return NotImplemented

    def ge(self, other):
        """
        Automatically created by characteristic.
        """
        if isinstance(other, self.__class__):
            return attrs_to_tuple(self) >= attrs_to_tuple(other)
        else:
            return NotImplemented

    def hash_(self):
        """
        Automatically created by characteristic.
        """
        return hash(attrs_to_tuple(self))

    def wrap(cl):
        cl.__eq__ = eq
        cl.__ne__ = ne
        cl.__lt__ = lt
        cl.__le__ = le
        cl.__gt__ = gt
        cl.__ge__ = ge
        cl.__hash__ = hash_

        return cl
    return wrap


def with_repr(attrs):
    """
    A class decorator that adds a human readable ``__repr__`` method to your
    class using *attrs*.

    :param attrs: Attributes to work with.
    :type attrs: ``list`` of native strings
    """
    def repr_(self):
        """
        Automatically created by characteristic.
        """
        return "<{0}({1})>".format(
            self.__class__.__name__,
            ", ".join(a + "=" + repr(getattr(self, a)) for a in attrs)
        )

    def wrap(cl):
        cl.__repr__ = repr_
        return cl

    return wrap


def with_init(attrs, defaults=None):
    """
    A class decorator that wraps the ``__init__`` method of a class and sets
    *attrs* using passed *keyword arguments* before calling the original
    ``__init__``.

    Those keyword arguments that are used, are removed from the `kwargs` that
    is passed into your original ``__init__``.  Optionally, a dictionary of
    default values for some of *attrs* can be passed too.

    :param attrs: Attributes to work with.
    :type attrs: ``list`` of native strings

    :param defaults: Default values if attributes are omitted on instantiation.
    :type defaults: ``dict`` or ``None``

    :raises ValueError: If the value for a non-optional attribute hasn't been
        passed as a keyword argument.
    """
    if defaults is None:
        defaults = {}

    def init(self, *args, **kw):
        """
        Attribute initializer automatically created by characteristic.

        The original `__init__` method is renamed to `__original_init__` and
        is called at the end.
        """
        try:
            for a in attrs:
                if a in defaults:
                    v = kw.pop(a, defaults[a])
                else:
                    v = kw.pop(a)
                setattr(self, a, v)
        except KeyError as e:
            raise ValueError(
                "Missing keyword value for '{0}'.".format(e.args[0])
            )

        self.__original_init__(*args, **kw)

    def wrap(cl):
        cl.__original_init__ = cl.__init__
        cl.__init__ = init
        return cl

    return wrap


_ERR_MIXING = ("Mixing of Attribute()-style and decorator-style definition of "
               "attributes is prohibited.")


def attributes(attrs_or_class=None, defaults=None, create_init=True):
    """
    A convenience class decorator that combines :func:`with_cmp`,
    :func:`with_repr`, and optionally :func:`with_init` to avoid code
    duplication.

    See :doc:`examples` for ``@attributes`` in action!

    It can be used both for defining attributes using :class:`Attribute()`s and
    the `attrs` argument.  Mixing is not allowed though.

    :param attrs: Attributes to work with.
    :type attrs: ``list`` of native strings.

    :param defaults: Default values if attributes are omitted on instantiation.
        Can be only used together with `attrs`.
    :type defaults: ``dict`` or ``None``

    :param create_init: Also apply :func:`with_init` (default: ``True``)
    :type create_init: ``bool``

    :raises ValueError: If the value for a non-optional attribute hasn't been
        passed as a keyword argument.
    :raises ValueError: If the :class:`Attribute()`-as-class-attributes-style
        and the @attributes([])-style are mixed.
    """

    # attrs_or class type depends on the usage of the decorator.
    # It's a class if it's used as `@attributes` but ``None`` (or a value
    # passed) # if used as `@attributes()`.
    if isinstance(attrs_or_class, type):
        a = _get_attributes(attrs_or_class)
        new_cl = with_cmp(a.attrs)(with_repr(a.attrs)(attrs_or_class))
        if create_init is True:
            new_cl = with_init(a.attrs, defaults=a.defaults)(new_cl)

        return new_cl
    else:
        def wrap(cl):
            # nonlocal would be awesome :(
            if defaults is None:
                defaults_ = {}
            else:
                defaults_ = defaults

            a = _get_attributes(cl)
            if attrs_or_class is None:
                if defaults_ != {}:
                    raise ValueError(_ERR_MIXING)

                attrs = a.attrs
                defaults_ = a.defaults
            else:
                if a.attrs != []:
                    raise ValueError(_ERR_MIXING)

                attrs = attrs_or_class

            new_cl = with_cmp(attrs)(with_repr(attrs)(cl))
            if create_init is True:
                return with_init(attrs, defaults=defaults_)(new_cl)
            else:
                return new_cl

    return wrap


class _Attributes(object):
    def __init__(self, attrs, defaults):
        self.attrs = attrs
        self.defaults = defaults


def _get_attributes(cl):
    """
    :rtype: _Attributes
    """
    attrs = []
    defaults = {}
    for name, instance in sorted((
            (n, i) for n, i in cl.__dict__.items() if isinstance(i, Attribute)
    ), key=lambda e: e[1].counter):
        attrs.append(name)
        if instance.default is not NOTHING:
            defaults[name] = instance.default
    return _Attributes(attrs, defaults)
