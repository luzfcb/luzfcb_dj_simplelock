#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_luzfcb_dj_simplelock
------------

Tests for `luzfcb_dj_simplelock` views module.
"""

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import override_settings
from sample_project.app_test.models import Person

from luzfcb_dj_simplelock.utils import get_label
from luzfcb_dj_simplelock.views import DEFAULT_LOCK_DELETE_FORM_PREFIX

from .utils import SplinterStaticLiveServerTestCase


@override_settings(DEBUG=True)
class MeuTesteDeAceitacao(SplinterStaticLiveServerTestCase):
    use_virtual_display = False

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
        # ugly monkeypatch
        import luzfcb_dj_simplelock
        luzfcb_dj_simplelock.views.DEFAULT_LOCK_EXPIRE_TIME_IN_SECONDS = self.lock_expire_time_in_seconds

        self.model_instance = Person.objects.create(nome="Maria")
        self.model_instance_app_label = get_label(self.model_instance)
        self.user1 = User.objects.create_superuser(**self.user1_data)
        self.user2 = User.objects.create_superuser(**self.user2_data)
        self.view_url = reverse('person:editar', kwargs={'pk': self.model_instance.pk})

    def test_open_url(self):
        self.login_as(username=self.user1_data['username'], password=self.user1_data['password'])
        self.wait_for_seconds(3)
        print("abrindo url")
        self.open(self.view_url)
        botao = self.browser.find_by_name('id_person_update_form_submit')
        botao.click()
        self.wait_for_seconds(5)
        self.open("{}?ajax='ajax'".format(self.view_url))
        botao = self.browser.find_by_name('id_person_update_form_submit')
        botao.click()
        self.wait_for_seconds(5)
