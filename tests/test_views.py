#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_luzfcb_dj_simplelock
------------

Tests for `luzfcb_dj_simplelock` views module.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from app_test.models import Person
from luzfcb_dj_simplelock.models import ObjectLock
from luzfcb_dj_simplelock.utils import get_label


class ExclusiveEditionGetNoLock(TestCase):
    def setUp(self):
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

        self.object = Person.objects.create(nome="Maria")
        self.object_app_label = get_label(self.object)
        self.user1 = User.objects.create_superuser(**self.user1_data)
        self.user2 = User.objects.create_superuser(**self.user2_data)
        self.request = self.client.get(reverse('pessoa:editar', kwargs={'pk': self.object.pk}))

    def test_foo(self):
        ObjectLock.objects.get(model_pk=self.object.pk, app_and_model=self.object_app_label)
        self.assertTrue(True, 'sertó mizeravi')
