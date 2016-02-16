#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_luzfcb_dj_simplelock
------------

Tests for `luzfcb_dj_simplelock` views module.
"""
import datetime
import json

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import override_settings
from rebar.testing import flatten_to_dict
from splinter import Browser

from sample_project.app_test.models import Person
from luzfcb_dj_simplelock.views import (lock_revalidate_form_id, lock_revalidate_form_prefix, lock_delete_form_id,
                                        lock_delete_form_prefix)
from luzfcb_dj_simplelock.models import ObjectLock
from luzfcb_dj_simplelock.utils import get_label
from luzfcb_dj_simplelock.forms import ReValidarForm, DeletarForm
from .utils import SplinterStaticLiveServerTestCase


@override_settings(DEBUG=True)
class MeuTesteDeAceitacao(SplinterStaticLiveServerTestCase):
    def setUp(self):
        super(MeuTesteDeAceitacao, self).setUp()
        # self.browser = Browser('firefox')
        self.user1_data = {
            'username': 'admin',
            'email': 'admin@admin.com',
            'password': 'admin',
            'first_name': 'Admin',
            'last_name': 'Root'
        }
        self.user2_data = {
            'username': 'maria',
            'email': 'maria@maria.com',
            'password': 'maria',
            'first_name': 'Maria',
            'last_name': 'Neo Matrix'
        }
        self.lock_expire_time_in_seconds = 2
        # ugly monkeypath
        import luzfcb_dj_simplelock
        luzfcb_dj_simplelock.views.lock_expire_time_in_seconds = self.lock_expire_time_in_seconds

        self.model_instance = Person.objects.create(nome="Maria")
        self.model_instance_app_label = get_label(self.model_instance)
        self.user1 = User.objects.create_superuser(**self.user1_data)
        self.user2 = User.objects.create_superuser(**self.user2_data)
        self.view_url = reverse('person:editar', kwargs={'pk': self.model_instance.pk})

    # def tearDown(self):
    #     super(MeuTesteDeAceitacao, self).tearDown()
    #     self.browser.quit()

    def test_open_url(self):
        self.login_as(browser=self.browser, username=self.user1_data['username'], password=self.user1_data['password'])
        self.open(self.view_url)

        self.wait_for_seconds(10)


