#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_luzfcb_dj_simplelock
------------

Tests for `luzfcb_dj_simplelock` views module.
"""
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rebar.testing import flatten_to_dict
from sample_project.app_test.models import Person

from luzfcb_dj_simplelock.forms import DeletarForm, ReValidarForm
from luzfcb_dj_simplelock.models import ObjectLock
from luzfcb_dj_simplelock.utils import get_label
from luzfcb_dj_simplelock.views import (
    default_lock_delete_form_id, default_lock_delete_form_prefix,
    default_lock_revalidate_form_id, default_lock_revalidate_form_prefix,
)


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
        self.lock_expire_time_in_seconds = 2
        # ugly monkeypath
        import luzfcb_dj_simplelock
        luzfcb_dj_simplelock.views.default_lock_expire_time_in_seconds = self.lock_expire_time_in_seconds

        self.model_instance = Person.objects.create(nome="Maria")
        self.model_instance_app_label = get_label(self.model_instance)
        self.user1 = User.objects.create_superuser(**self.user1_data)
        self.user2 = User.objects.create_superuser(**self.user2_data)
        self.view_url = reverse('person:editar', kwargs={'pk': self.model_instance.pk})
        self.client.login(username=self.user1_data['username'], password=self.user1_data['password'])
        self.response = self.client.get(self.view_url)

    def test_lock_is_created_and_locked_to_user1(self):
        object_lock = ObjectLock.objects.get(model_pk=self.model_instance.pk,
                                             app_and_model=self.model_instance_app_label)
        self.assertTrue(object_lock.bloqueado_por == self.user1, "Nao é o usuario que bloqueou")

    def test_locked_to_user1_and_user2_should_be_redirected_to_detail_view(self):
        object_lock = ObjectLock.objects.get(model_pk=self.model_instance.pk,
                                             app_and_model=self.model_instance_app_label)
        self.client.logout()
        self.client.login(username=self.user2_data['username'], password=self.user2_data['password'])
        response2 = self.client.get(self.view_url, follow=True)

        self.assertFalse(object_lock.bloqueado_por == self.user2, "Nao é o usuario que bloqueou")
        self.assertContains(response2, text='Disponivel somente para visualização', status_code=200)

    def test_ajax_sucess_revalidate_lock(self):
        revalidar_form = ReValidarForm(prefix=default_lock_revalidate_form_prefix,
                                       initial={'hash': self.model_instance.pk, 'id': self.model_instance.pk})

        data = flatten_to_dict(revalidar_form)
        data.update({str(default_lock_revalidate_form_id): str(default_lock_revalidate_form_id)})
        response_post = self.client.post(path=self.view_url,
                                         data=data,
                                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(json.loads(response_post.content.decode()),
                         {"status": "success", "id": self.model_instance.pk, "mensagem": "revalidado com sucesso"})

        from time import sleep
        sleep(self.lock_expire_time_in_seconds)
        response_post = self.client.post(path=self.view_url,
                                         data=data,
                                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(json.loads(response_post.content.decode()),
                         {"status": "success", "id": self.model_instance.pk, "mensagem": "revalidado com sucesso"})

    def test_ajax_fail_revalidate_lock(self):
        revalidar_form = ReValidarForm(prefix=default_lock_revalidate_form_prefix,
                                       initial={'hash': 'errado', 'id': self.model_instance.pk})

        data = flatten_to_dict(revalidar_form)
        data.update({str(default_lock_revalidate_form_id): str(default_lock_revalidate_form_id)})
        response_post = self.client.post(path=self.view_url,
                                         data=data,
                                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(json.loads(response_post.content.decode()),
                         {"status": "fail", "id": self.model_instance.pk, "mensagem": "erro ao revalidar"})

    # def test_ajax_generic_fail(self):
    #     response_post = self.client.post(path=self.view_url,
    #                                      data={'foo': 'bar'},
    #                                      HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #
    #     self.assertEqual(json.loads(response_post.content.decode()),
    #                      {"status": "fail", "id": self.model_instance.pk, "mensagem": "post_invalido"})

    def test_ajax_sucess_deletar_lock(self):
        deletar_form = DeletarForm(prefix=default_lock_delete_form_prefix,
                                   initial={'hash': self.model_instance.pk, 'id': self.model_instance.pk})

        data = flatten_to_dict(deletar_form)
        data.update({str(default_lock_delete_form_id): str(default_lock_delete_form_id)})
        response_post = self.client.post(path=self.view_url,
                                         data=data,
                                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(json.loads(response_post.content.decode()),
                         {"status": "success", "id": self.model_instance.pk, "mensagem": "deletado com sucesso"})

    def test_ajax_fail_deletar_lock(self):
        deletar_form = DeletarForm(prefix=default_lock_delete_form_prefix,
                                   initial={'hash': 'errado', 'id': self.model_instance.pk})

        data = flatten_to_dict(deletar_form)
        data.update({str(default_lock_delete_form_id): str(default_lock_delete_form_id)})
        response_post = self.client.post(path=self.view_url,
                                         data=data,
                                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(json.loads(response_post.content.decode()),
                         {"status": "fail", "id": self.model_instance.pk, "mensagem": "erro ao deletar"})

    def test_expire_lock(self):
        object_lock_original = ObjectLock.objects.get(model_pk=self.model_instance.pk,
                                                      app_and_model=self.model_instance_app_label)
        from time import sleep
        sleep(self.lock_expire_time_in_seconds + 1)

        self.client.logout()
        self.client.login(username=self.user2_data['username'], password=self.user2_data['password'])
        response2 = self.client.get(self.view_url, follow=True)
        object_lock = ObjectLock.objects.get(model_pk=self.model_instance.pk,
                                             app_and_model=self.model_instance_app_label)

        # print(object_lock_original)
        # print(object_lock)
        self.assertFalse(object_lock.bloqueado_por == self.user1, "Nao é o usuario que bloqueou")
