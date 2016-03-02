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



Run `python manage.py migrate`

Use Mixin::

    from luzfcb_dj_simplelock.views import LuzfcbLockMixin

    class MyView(LuzfcbLockMixin, UpdateView):
        #
        lock_expire_time_in_seconds = 30
        lock_revalidated_at_every_x_seconds = 25

        lock_use_builtin_jquery = False
        lock_use_builtin_jquery_csrftoken = False
        model = Person

        def get_lock_url_to_redirect_if_locked(self):
            return reverse('person:detail', kwargs={'pk': self.object.pk})


In your template, add this "include" after load JQuery and csrftoken configuration to ajax form post::


     {% include 'luzfcb_dj_simplelock/dj_simplelock.html' %}



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

