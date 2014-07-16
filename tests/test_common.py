from __future__ import absolute_import, division, print_function

import pytest

from characteristic._common import (
    Attribute,
    Nothing,
    attributes,
)


class TestAttribute(object):
    def test_converts_into_attrs_list(self):
        """
        Specifying using class variables works.
        """
        @attributes()
        class Class(object):
            a = Attribute()
            b = Attribute()

        i = Class(a=42, b=23)
        assert 42 == i.a
        assert 23 == i.b

    def test_defaults(self):
        """
        defaults work.
        """
        @attributes()
        class Class(object):
            a = Attribute(default=23)

        assert 23 == Class().a
        assert 46 == Class(a=46).a

    def test_works_without_parens(self):
        """
        @attributes
        class C(object)):

        is equivalent to

        @attributes()
        class C(object):
        """
        @attributes
        class Class(object):
            a = Attribute()

        i = Class(a=42)
        assert 42 == i.a

    def test_mixing_attrs(self):
        """
        Mixing of Attribute()-style and @attributes([]) raises ValueError.
        """
        with pytest.raises(ValueError):
            @attributes(["a"])
            class Class(object):
                b = Attribute()

    def test_mixing_defaults(self):
        """
        Using the defaults argument of @attributes with Attribute()-style
        definition raises ValueError.
        """
        with pytest.raises(ValueError):
            @attributes(defaults={"a": 42})
            class Class(object):
                a = Attribute()

    def test_no_init(self):
        """
        create_init=False works and no __init__ is created.  That means that
        the attributes are still `Attribute()`\ s as class attributes.
        """
        @attributes(create_init=False)
        class Class(object):
            a = Attribute()
        assert isinstance(Class().a, Attribute)

    def test_no_cmp(self):
        """
        create_cmp=False works and not comparasition methods are created.
        """
        @attributes(create_cmp=False)
        class Class(object):
            a = Attribute()
        eq = getattr(Class(a=1), "__eq__", None)
        if eq is not None:
            assert Class.__eq__ is object.__eq__

    def test_no_repr(self):
        """
        create_repr=False works and no __repr__ method is created.
        """
        @attributes(create_repr=False)
        class Class(object):
            a = Attribute()
        assert repr(Class(a=1)).startswith("<tests.test_common.")

    def test_order(self):
        """
        The order of the attributes is maintained.

        Due to dict's nature of non-deterministic order this is difficult to
        really test.
        """
        @attributes
        class Class(object):
            c = Attribute()
            a = Attribute()
            d = Attribute()
            b = Attribute()

        assert "<Class(c=3, a=1, d=4, b=2)>" == repr(Class(a=1, b=2, c=3, d=4))


def test_nothing():
    """
    ``Nothing`` has a sensible repr.
    """
    assert "<Nothing()>" == repr(Nothing())
