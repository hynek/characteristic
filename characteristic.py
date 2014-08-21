from __future__ import absolute_import, division, print_function

"""
Python attributes without boilerplate.
"""

import sys
import warnings


__version__ = "14.0.0"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2014 Hynek Schlawack"

__all__ = [
    "Attribute",
    "NOTHING",
    "attributes",
    "immutable",
    "strip_leading_underscores",
    "with_cmp",
    "with_init",
    "with_repr",
]


class _Nothing(object):
    """
    Sentinel class to indicate the lack of a value when ``None`` is ambiguous.

    .. versionadded:: 14.0
    """
    def __repr__(self):
        return "NOTHING"


NOTHING = _Nothing()
"""
Sentinel to indicate the lack of a value when ``None`` is ambiguous.

.. versionadded:: 14.0
"""


def strip_leading_underscores(attribute_name):
    """
    Strip leading underscores from *attribute_name*.

    Used by default by the ``init_aliaser`` argument of :class:`Attribute`.

    :param attribute_name: The original attribute name to mangle.
    :type attribute_name: str

    :rtype: str
    """
    return attribute_name.lstrip("_")


class Attribute(object):
    """
    A representation of an attribute.

    In the simplest case, it only consists of a name but more advanced
    properties like default values are possible too.

    All attributes on the Attribute class are *read-only*.

    :param name: Name of the attribute.
    :type name: str

    :param exclude_from_cmp: Ignore attribute in :func:`with_cmp`.
    :type exclude_from_cmp: bool

    :param exclude_from_init: Ignore attribute in :func:`with_init`.
    :type exclude_from_init: bool

    :param exclude_from_repr: Ignore attribute in :func:`with_repr`.
    :type exclude_from_repr: bool

    :param exclude_from_immutable: Ignore attribute in :func:`immutable`.
    :type exclude_from_immutable: bool

    :param default_value: A value that is used whenever this attribute isn't
        passed as an keyword argument to a class that is decorated using
        :func:`with_init` (or :func:`attributes` with
        ``apply_with_init=True``).

        Therefore, setting this makes an attribute *optional*.

        Since a default value of `None` would be ambiguous, a special sentinel
        :data:`NOTHING` is used.  Passing it means the lack of a default value.

    :param default_factory: A factory that is used for generating default
        values whenever this attribute isn't passed as an keyword
        argument to a class that is decorated using :func:`with_init` (or
        :func:`attributes` with ``apply_with_init=True``).

        Therefore, setting this makes an attribute *optional*.
    :type default_factory: callable

    :param instance_of: If used together with :func:`with_init` (or
        :func:`attributes` with ``apply_with_init=True``), the passed value is
        checked whether it's an instance of the type passed here.  The
        initializer then raises :exc:`TypeError` on mismatch.
    :type instance_of: type

    :param init_aliaser: A callable that is invoked with the name of the
        attribute and whose return value is used as the keyword argument name
        for the ``__init__`` created by :func:`with_init` (or
        :func:`attributes` with ``apply_with_init=True``).  Uses
        :func:`strip_leading_underscores` by default to change ``_foo`` to
        ``foo``.  Set to ``None`` to disable aliasing.
    :type init_aliaser: callable

    :raises ValueError: If both ``default_value`` and ``default_factory`` have
        been passed.

    .. versionadded:: 14.0
    """
    __slots__ = [
        "name", "exclude_from_cmp", "exclude_from_init", "exclude_from_repr",
        "exclude_from_immutable", "default_value", "default_factory",
        "instance_of", "init_aliaser", "_default", "_kw_name",
    ]

    def __init__(self,
                 name,
                 exclude_from_cmp=False,
                 exclude_from_init=False,
                 exclude_from_repr=False,
                 exclude_from_immutable=False,
                 default_value=NOTHING,
                 default_factory=None,
                 instance_of=None,
                 init_aliaser=strip_leading_underscores):
        if (
                default_value is not NOTHING
                and default_factory is not None
        ):
            raise ValueError(
                "Passing both default_value and default_factory is "
                "ambiguous."
            )

        self.name = name
        self.exclude_from_cmp = exclude_from_cmp
        self.exclude_from_init = exclude_from_init
        self.exclude_from_repr = exclude_from_repr
        self.exclude_from_immutable = exclude_from_immutable

        self.default_value = default_value
        self.default_factory = default_factory
        if default_value is not NOTHING:
            self._default = default_value
        elif default_factory is None:
            self._default = NOTHING

        self.instance_of = instance_of

        self.init_aliaser = init_aliaser
        if init_aliaser is not None:
            self._kw_name = init_aliaser(name)
        else:
            self._kw_name = name

    def __getattr__(self, name):
        """
        If no value has been set to _default, we need to call a factory.
        """
        if name == "_default" and self.default_factory:
            return self.default_factory()
        else:
            raise AttributeError

    def __repr__(self):
        return (
            "<Attribute(name={name!r}, exclude_from_cmp={exclude_from_cmp!r}, "
            "exclude_from_init={exclude_from_init!r}, exclude_from_repr="
            "{exclude_from_repr!r}, exclude_from_immutable="
            "{exclude_from_immutable!r}, default_value={default_value!r}, "
            "default_factory={default_factory!r}, instance_of={instance_of!r},"
            " init_aliaser={init_aliaser!r})>"
        ).format(
            name=self.name, exclude_from_cmp=self.exclude_from_cmp,
            exclude_from_init=self.exclude_from_init,
            exclude_from_repr=self.exclude_from_repr,
            exclude_from_immutable=self.exclude_from_immutable,
            default_value=self.default_value,
            default_factory=self.default_factory, instance_of=self.instance_of,
            init_aliaser=self.init_aliaser,
        )


def _ensure_attributes(attrs):
    """
    Return a list of :class:`Attribute` generated by creating new instances for
    all non-Attributes.
    """
    return [
        Attribute(a, init_aliaser=None)
        if not isinstance(a, Attribute) else a
        for a in attrs
    ]


def with_cmp(attrs):
    """
    A class decorator that adds comparison methods based on *attrs*.

    For that, each class is treated like a ``tuple`` of the values of *attrs*.
    But only instances of *identical* classes are compared!

    :param attrs: Attributes to work with.
    :type attrs: :class:`list` of :class:`str` or :class:`Attribute`\ s.
    """
    def attrs_to_tuple(obj):
        """
        Create a tuple of all values of *obj*'s *attrs*.
        """
        return tuple(getattr(obj, a.name) for a in attrs)

    def eq(self, other):
        """
        Automatically created by characteristic.
        """
        if other.__class__ is self.__class__:
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
        if other.__class__ is self.__class__:
            return attrs_to_tuple(self) < attrs_to_tuple(other)
        else:
            return NotImplemented

    def le(self, other):
        """
        Automatically created by characteristic.
        """
        if other.__class__ is self.__class__:
            return attrs_to_tuple(self) <= attrs_to_tuple(other)
        else:
            return NotImplemented

    def gt(self, other):
        """
        Automatically created by characteristic.
        """
        if other.__class__ is self.__class__:
            return attrs_to_tuple(self) > attrs_to_tuple(other)
        else:
            return NotImplemented

    def ge(self, other):
        """
        Automatically created by characteristic.
        """
        if other.__class__ is self.__class__:
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

    attrs = [a
             for a in _ensure_attributes(attrs)
             if a.exclude_from_cmp is False]
    return wrap


def with_repr(attrs):
    """
    A class decorator that adds a human readable ``__repr__`` method to your
    class using *attrs*.

    :param attrs: Attributes to work with.
    :type attrs: ``list`` of :class:`str` or :class:`Attribute`\ s.
    """
    def repr_(self):
        """
        Automatically created by characteristic.
        """
        return "<{0}({1})>".format(
            self.__class__.__name__,
            ", ".join(a.name + "=" + repr(getattr(self, a.name))
                      for a in attrs)
        )

    def wrap(cl):
        cl.__repr__ = repr_
        return cl

    attrs = [a
             for a in _ensure_attributes(attrs)
             if a.exclude_from_repr is False]
    return wrap


def with_init(attrs, **kw):
    """
    A class decorator that wraps the ``__init__`` method of a class and sets
    *attrs* using passed *keyword arguments* before calling the original
    ``__init__``.

    Those keyword arguments that are used, are removed from the `kwargs` that
    is passed into your original ``__init__``.  Optionally, a dictionary of
    default values for some of *attrs* can be passed too.

    Attributes that are defined using :class:`Attribute` and start with
    underscores will get them stripped for the initializer arguments by default
    (this behavior is changeable on per-attribute basis when instantiating
    :class:`Attribute`.

    :param attrs: Attributes to work with.
    :type attrs: ``list`` of :class:`str` or :class:`Attribute`\ s.

    :raises ValueError: If the value for a non-optional attribute hasn't been
        passed as a keyword argument.
    :raises ValueError: If both *defaults* and an instance of
        :class:`Attribute` has been passed.

    .. deprecated:: 14.0
        Use :class:`Attribute` instead of ``defaults``.

    :param defaults: Default values if attributes are omitted on instantiation.
    :type defaults: ``dict`` or ``None``
    """
    if "defaults" not in kw:
        defaults = {}
    else:
        defaults = kw["defaults"] or {}
        warnings.warn(
            "`defaults` has been deprecated in 14.0,  please use the "
            "`Attribute` class instead.",
            DeprecationWarning
        )

    def characteristic_init(self, *args, **kw):
        """
        Attribute initializer automatically created by characteristic.

        The original `__init__` method is renamed to `__original_init__` and
        is called at the end with the initialized attributes removed from the
        keyword arguments.
        """
        for a in attrs:
            v = kw.pop(a._kw_name, NOTHING)
            if v is NOTHING:
                # Since ``a._default`` could be a property that calls
                # a factory, we make this a separate step.
                v = a._default
            if v is NOTHING:
                raise ValueError(
                    "Missing keyword value for '{0}'.".format(a._kw_name)
                )
            if (
                a.instance_of is not None
                and not isinstance(v, a.instance_of)
            ):
                    raise TypeError(
                        "Attribute '{0}' must be an instance of '{1}'."
                        .format(a.name, a.instance_of.__name__)
                    )
            self.__characteristic_setattr__(a.name, v)
        self.__original_init__(*args, **kw)

    def wrap(cl):
        cl.__original_init__ = cl.__init__
        cl.__init__ = characteristic_init
        # Sidestep immutability sentry completely if possible..
        cl.__characteristic_setattr__ = getattr(
            cl, "__original_setattr__", cl.__setattr__
        )
        return cl

    new_attrs = []
    for a in attrs:
        if isinstance(a, Attribute):
            if defaults != {}:
                raise ValueError(
                    "Mixing of the 'defaults' keyword argument and passing "
                    "instances of Attribute for 'attrs' is prohibited.  "
                    "Please don't use 'defaults' anymore, it has been "
                    "deprecated in 14.0."
                )
            if not a.exclude_from_init:
                new_attrs.append(a)
        else:
            default_value = defaults.get(a)
            if default_value:
                new_attrs.append(
                    Attribute(
                        a,
                        default_value=default_value,
                        init_aliaser=None,
                    )
                )
            else:
                new_attrs.append(Attribute(a, init_aliaser=None))

    attrs = new_attrs
    return wrap


_VALID_INITS = frozenset(["characteristic_init", "__init__"])


def immutable(attrs):
    """
    Class decorator that makes *attrs* of a class immutable.

    That means that *attrs* can only be set from an initializer.  If anyone
    else tries to set one of them, an :exc:`AttributeError` is raised.

    .. versionadded:: 14.0
    """
    # In this case, we just want to compare (native) strings.
    attrs = frozenset(attr.name if isinstance(attr, Attribute) else attr
                      for attr in _ensure_attributes(attrs)
                      if attr.exclude_from_immutable is False)

    def characteristic_immutability_sentry(self, attr, value):
        """
        Immutability sentry automatically created by characteristic.

        If an attribute is attempted to be set from any other place than an
        initializer, a TypeError is raised.  Else the original __setattr__ is
        called.
        """
        prev = sys._getframe().f_back
        if (
            attr not in attrs
            or
            prev is not None and prev.f_code.co_name in _VALID_INITS
        ):
            self.__original_setattr__(attr, value)
        else:
            raise AttributeError(
                "Attribute '{0}' of class '{1}' is immutable."
                .format(attr, self.__class__.__name__)
            )

    def wrap(cl):
        cl.__original_setattr__ = cl.__setattr__
        cl.__setattr__ = characteristic_immutability_sentry
        return cl

    return wrap


def attributes(attrs, apply_with_cmp=True, apply_with_init=True,
               apply_with_repr=True, apply_immutable=False, **kw):
    """
    A convenience class decorator that allows to *selectively* apply
    :func:`with_cmp`, :func:`with_repr`, :func:`with_init`, and
    :func:`immutable` to avoid code duplication.

    :param attrs: Attributes to work with.
    :type attrs: ``list`` of :class:`str` or :class:`Attribute`\ s.

    :param apply_with_cmp: Apply :func:`with_cmp`.
    :type apply_with_cmp: bool

    :param apply_with_init: Apply :func:`with_init`.
    :type apply_with_init: bool

    :param apply_with_repr: Apply :func:`with_repr`.
    :type apply_with_repr: bool

    :param apply_immutable: Apply :func:`immutable`.  The only one that is off
        by default.
    :type apply_immutable: bool

    :raises ValueError: If both *defaults* and an instance of
        :class:`Attribute` has been passed.

    .. versionadded:: 14.0
        Added possibility to pass instances of :class:`Attribute` in ``attrs``.

    .. versionadded:: 14.0
        Added ``apply_*``.

    .. deprecated:: 14.0
        Use :class:`Attribute` instead of ``defaults``.

    :param defaults: Default values if attributes are omitted on instantiation.
    :type defaults: ``dict`` or ``None``

    .. deprecated:: 14.0
        Use ``apply_with_init`` instead of ``create_init``.  Until removal, if
        *either* if `False`, ``with_init`` is not applied.

    :param create_init: Apply :func:`with_init`.
    :type create_init: bool
    """
    if "create_init" in kw:
        apply_with_init = kw["create_init"]
        warnings.warn(
            "`create_init` has been deprecated in 14.0, please use "
            "`apply_with_init`.", DeprecationWarning
        )

    def wrap(cl):
        if apply_with_repr is True:
            cl = with_repr(attrs)(cl)
        if apply_with_cmp is True:
            cl = with_cmp(attrs)(cl)
        # Order matters here because with_init can optimize and side-step
        # immutable's sentry function.
        if apply_immutable is True:
            cl = immutable(attrs)(cl)
        if apply_with_init is True:
            cl = with_init(attrs, defaults=kw.get("defaults"))(cl)
        return cl
    return wrap
