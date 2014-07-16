from __future__ import absolute_import, division, print_function


from ._legacy import (
    with_cmp,
    with_repr,
    with_init,
)


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


def _get_attributes(cl):
    """
    Transitional helper that converts a class with Attribute-defined attributes
    into a list of attributes and a dictionary of default values.

    It will be pruned as soon as the new-style approach doesn't use the
    legacy decorators underneath.

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


class _Attributes(object):
    def __init__(self, attrs, defaults):
        self.attrs = attrs
        self.defaults = defaults
