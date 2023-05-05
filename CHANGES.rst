
These changes are listed in decreasing version number order.

Release 0.3.3
-------------

Release date was |today|

* fixing `tuple` as `list` issue for nested tuples and list.

Release 0.3.2
-------------

Release date was Friday, 05 May 2023

* fixing `tuple` as `list` issue for nested tuples.


Release 0.3.1
-------------

Release date was Friday, 05 May 2023

* fixing `tuple` as `list` issue by `loads(dumps((1, 2)))==[1, 2]`.
  Now every `tuple` or `set` is asserted as a `list`.


Release 0.3
-----------

Release date was Sunday, 21 November 2021

* control compression by class property


Release 0.2
-----------

Release date was Thursday, 7 October 2021

* dropping python 2 support

* store regression data in one file per each test method (than each class)

* made it a `auxilium <https://auxilium.readthedocs.io/en/latest/intro.html>`_ project

* a bit more documentation

Release 0.1
-----------

Release date was Wednesday, 18 September 2019
