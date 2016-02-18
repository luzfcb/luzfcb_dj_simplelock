=============================
luzfcb_dj_simplelock
=============================

.. image:: https://badge.fury.io/py/luzfcb_dj_simplelock.png
    :target: https://badge.fury.io/py/luzfcb_dj_simplelock

.. image:: https://travis-ci.org/luzfcb/luzfcb_dj_simplelock.png?branch=master
    :target: https://travis-ci.org/luzfcb/luzfcb_dj_simplelock

.. image:: https://codecov.io/github/luzfcb/luzfcb_dj_simplelock/coverage.svg?branch=master
    :target: https://codecov.io/github/luzfcb/luzfcb_dj_simplelock?branch=master

para evitar edição concorrente, concede temporariamente a capacidade de edição exclusiva de uma instancia de um model para um determinado usuario

Documentation
-------------

The full documentation is at https://luzfcb_dj_simplelock.readthedocs.org.

Quickstart
----------

Install luzfcb_dj_simplelock::

    pip install -e git+https://github.com/luzfcb/luzfcb_dj_simplelock.git#egg=luzfcb_dj_simplelock


Then use it in a project

Add 'luzfcb_dj_simplelock.apps.DjSimpleLockAppConfig' to yourINSTALLED_APPS::

    INSTALLED_APPS = [
        ...
        'luzfcb_dj_simplelock.apps.DjSimpleLockAppConfig',
        ..
    ]

    from luzfcb_dj_simplelock.views import LuzfcbLockMixin

    class MyView(LuzfcbLockMixin, UpdateView):
        model = Person



Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
