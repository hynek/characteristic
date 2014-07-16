from __future__ import absolute_import, division, print_function

"""
Python attributes without boilerplate.
"""


__version__ = "14.0.0dev"
__author__ = "Hynek Schlawack"
__license__ = "MIT"
__copyright__ = "Copyright 2014 Hynek Schlawack"


from ._common import (
    Attribute,
    attributes,
)


from ._legacy import (
    with_cmp,
    with_repr,
    with_init,
)


__all__ = [
    "Attribute",
    "attributes",
    "with_cmp",
    "with_init",
    "with_repr",
]
