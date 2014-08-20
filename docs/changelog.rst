Changelog
=========

- :feature:`-` Add possibility to disable single attributes from certain decorators.
- :feature:`12` Add type checks to :func:`~characteristic.with_init`\’s initializer.
- :feature:`13` Add aliasing of private attributes for :func:`~characteristic.with_init`\’s initializer when used together with :class:`~characteristic.Attribute`.
- :feature:`14` Add :func:`~characteristic.immutable` to make certain attributes of classes immutable.
  Also add ``make_immutable`` argument to :func:`~characteristic.attributes`.
- :feature:`8` Add explicit :class:`~characteristic.Attribute` class and use it for default factories.
  Deprecate the ``defaults`` argument of :func:`~characteristic.with_init` and :func:`~characteristic.attributes`.
- :support:`-` Switch to a year-based version scheme.
- :release:`0.1.0 <2014-05-11>`
- :feature:`-` Initial work.
