Changelog
=========

- :release:`14.0.0 <2014-08-21>`
- :feature:`-` Add possibility to hand-pick which decorators are applied from within :func:`~characteristic.attributes`.
  A new line of arguments has been introduced for that and ``create_init`` has been deprecated.
- :feature:`-` Add possibility to exclude single attributes from certain decorators.
- :feature:`12` Add type checks to :func:`~characteristic.with_init`\’s initializer.
- :feature:`13` Add aliasing of private attributes for :func:`~characteristic.with_init`\’s initializer when used together with :class:`~characteristic.Attribute`.
  Allow for custom aliasing via a callable.
- :feature:`14` Add :func:`~characteristic.immutable` to make certain attributes of classes immutable.
  Also add ``apply_immutable`` argument to :func:`~characteristic.attributes`.
- :feature:`8` Add explicit :class:`~characteristic.Attribute` class and use it for default factories.
  Deprecate the ``defaults`` argument of :func:`~characteristic.with_init` and :func:`~characteristic.attributes`.
- :support:`-` Switch to a year-based version scheme.
- :release:`0.1.0 <2014-05-11>`
- :feature:`-` Initial work.
