.. currentmodule:: characteristic

.. :changelog:

Changelog
=========

Versions are year-based with a strict backwards-compatibility policy.
The third digit is only for regressions.


14.2.0 (2014-10-30)
-------------------


Backward-incompatible changes:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*none*


Deprecations:
^^^^^^^^^^^^^

*none*


Changes:
^^^^^^^^

- Attributes set by :func:`characteristic.attributes` are now stored on the class as well.
  [`20 <https://github.com/hynek/characteristic/pull/20>`_]
- ``__init__`` methods that are created by :func:`characteristic.with_init` are now generated on the fly and optimized for each class.
  [`9 <https://github.com/hynek/characteristic/pull/9>`_]


----


14.1.0 (2014-08-22)
-------------------


Backward-incompatible changes:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*none*


Deprecations:
^^^^^^^^^^^^^

*none*


Changes:
^^^^^^^^

- Fix stray deprecation warnings.
- Don't rely on warnings being switched on by command line.
  [`17 <https://github.com/hynek/characteristic/issues/17>`_]


----


14.0.0 (2014-08-21)
-------------------


Backward-incompatible changes:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*none*


Deprecations:
^^^^^^^^^^^^^

- The ``defaults`` argument of :func:`~characteristic.with_init` and :func:`~characteristic.attributes` has been deprecated in favor of the new explicit :class:`~characteristic.Attribute` class and it's superior ``default_value`` and ``default_factory`` arguments.
- The ``create_init`` argument of :func:`~characteristic.attributes` has been deprecated in favor of the new ``apply_with_init`` argument for the sake of consistency.


Changes:
^^^^^^^^

- Switch to a year-based version scheme.
- Add :func:`~characteristic.immutable` to make certain attributes of classes immutable.
  Also add ``apply_immutable`` argument to :func:`~characteristic.attributes`.
  [`14 <https://github.com/hynek/characteristic/issues/14>`_]
- Add explicit :class:`~characteristic.Attribute` class and use it for default factories.
  [`8 <https://github.com/hynek/characteristic/issues/8>`_]
- Add aliasing of private attributes for :func:`~characteristic.with_init`\’s initializer when used together with :class:`~characteristic.Attribute`.
  Allow for custom aliasing via a callable.
  [`6 <https://github.com/hynek/characteristic/issues/6>`_, `13 <https://github.com/hynek/characteristic/issues/13>`_]
- Add type checks to :func:`~characteristic.with_init`\’s initializer.
  [`12 <https://github.com/hynek/characteristic/issues/13>`_]
- Add possibility to hand-pick which decorators are applied from within :func:`~characteristic.attributes`.
- Add possibility to exclude single attributes from certain decorators.


----


0.1.0 (2014-05-11)
------------------

- Initial release.
