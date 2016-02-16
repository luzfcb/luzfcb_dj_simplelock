# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import generic

from sample_project.app_test.models import Person

from .forms import DeletarForm, ReValidarForm
from .models import ObjectLock
from .utils import get_label

###################################################################################################################
lock_expire_time_in_seconds = 30
lock_revalidated_at_every_x_seconds = 5
lock_revalidate_form_id = 'id_revalidar_form'
lock_revalidate_form_prefix = 'revalidar'
lock_delete_form_id = 'id_deletar_form'
lock_delete_form_prefix = 'deletar'
update_view_str = 'person:editar'
detail_view_str = 'person:detail'

# Get an instance of a logger
logger = logging.getLogger(__name__)


def revalidate_lock(documento_lock, updated_values_dict):
    documento_lock.bloqueado_por = updated_values_dict['bloqueado_por']
    documento_lock.bloqueado_por_user_name = updated_values_dict['bloqueado_por_user_name']
    documento_lock.bloqueado_por_full_name = updated_values_dict['bloqueado_por_full_name']
    documento_lock.expire_date = updated_values_dict['expire_date']
    with transaction.atomic():
        documento_lock.save()


class LuzfcbLockMixin(object):
    template_name = 'app_test/person_update.html'
    model = Person
    fields = ('nome',)

    def get_success_url(self):
        return reverse('person:editar', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(LuzfcbLockMixin, self).get_context_data(**kwargs)

        revalidate_form = ReValidarForm(prefix=lock_revalidate_form_prefix,
                                        initial={'hash': self.object.pk, 'id': self.object.pk})
        delete_form = DeletarForm(prefix=lock_delete_form_prefix,
                                  initial={'hash': self.object.pk, 'id': self.object.pk})

        context.update(
            {
                'update_view_str': update_view_str,
                'delete_form_id': lock_delete_form_id,
                'delete_form': delete_form,
                'revalidate_form': revalidate_form,
                'revalidate_form_id': lock_revalidate_form_id,
                'revalidate_lock_at_every_x_seconds': lock_revalidated_at_every_x_seconds
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        original_response = super(LuzfcbLockMixin, self).get(request, *args, **kwargs)
        label = get_label(self.object)
        now_time = timezone.now()
        next_expire_time = now_time + timezone.timedelta(seconds=lock_expire_time_in_seconds)
        updated_values = {'model_pk': self.object.pk,
                          'app_and_model': label,
                          'bloqueado_por': request.user,
                          'bloqueado_por_user_name': request.user.username,
                          'bloqueado_por_full_name': request.user.get_full_name(),
                          # session_key: session.session_key,
                          'expire_date': next_expire_time}

        # obtem o registro de bloqueio existente ou cria um novo.
        # a obtencao ou criacao eh feita em uma unica transacao
        # assegurada que nao há concorrencia
        with transaction.atomic():
            documento_lock, created = ObjectLock.objects.get_or_create(defaults=updated_values,
                                                                       app_and_model=label,
                                                                       model_pk=self.object.pk)

        if request.method == 'GET':
            # verificar se nao ha bloqueio
            # se nao houver bloqueio, dar permissao de edicao exclusiva para o usuario da requisicao

            # se registro de bloqueio nao eh novo, e o ele ja expirou, atualiza o registro
            # para o usuario atual da requisicao e atualiza o novo tempo de expiracao
            if not created and documento_lock and now_time > documento_lock.expire_date:
                revalidate_lock(documento_lock, updated_values)

            # se usuario atual da requisicao for diferente do usuario o qual foi dado o bloqueio,
            # nao autoriza a edicao e redireciona para a pagina de visualizacao,
            # informando o usuario que o documento ja esta sendo editado
            if documento_lock and not documento_lock.bloqueado_por.pk == request.user.pk:
                detail_url = reverse(detail_view_str, kwargs={'pk': self.object.pk})
                msg = 'Documento está sendo editado por {} - Disponivel somente para visualização'.format(
                    documento_lock.bloqueado_por_full_name or documento_lock.bloqueado_por_user_name)
                messages.add_message(request, messages.INFO, msg)
                logger.debug(msg)
                # print(msg)
                return redirect(detail_url, permanent=False)

        return original_response

    def post(self, request, *args, **kwargs):
        original_response = super(LuzfcbLockMixin, self).post(request, *args, **kwargs)
        label = get_label(self.object)
        now_time = timezone.now()
        next_expire_time = now_time + timezone.timedelta(seconds=lock_expire_time_in_seconds)
        updated_values = {'model_pk': self.object.pk,
                          'app_and_model': label,
                          'bloqueado_por': request.user,
                          'bloqueado_por_user_name': request.user.username,
                          'bloqueado_por_full_name': request.user.get_full_name(),
                          # session_key: session.session_key,
                          'expire_date': next_expire_time}

        # obtem o registro de bloqueio existente ou cria um novo.
        # a obtencao ou criacao eh feita em uma unica transacao
        # assegurada que nao há concorrencia
        with transaction.atomic():
            documento_lock, created = ObjectLock.objects.get_or_create(defaults=updated_values,
                                                                       app_and_model=label,
                                                                       model_pk=self.object.pk)
        if request.is_ajax:

            revalidate_form = ReValidarForm(data=request.POST,
                                            files=request.FILES,
                                            prefix=lock_revalidate_form_prefix,
                                            id_obj=self.object.pk)
            delete_form = DeletarForm(data=request.POST,
                                      files=request.FILES,
                                      prefix=lock_delete_form_prefix,
                                      id_obj=self.object.pk)

            if lock_revalidate_form_id in request.POST and documento_lock.bloqueado_por.pk == request.user.pk:
                if revalidate_form.is_valid():
                    # se registro de bloqueio nao eh novo, e o ele ja expirou, atualiza o registro
                    # para o usuario atual da requisicao e atualiza o novo tempo de expiracao
                    if not created and documento_lock and now_time > documento_lock.expire_date:
                        revalidate_lock(documento_lock, updated_values)
                    # messages.add_message(request, messages.INFO, 'revalidado com sucesso')
                    # print('revalidado com sucesso')
                    return JsonResponse({
                        'mensagem': 'revalidado com sucesso',
                        'id': self.object.pk,
                        'status': 'success'
                    })
                else:
                    # messages.add_message(request, messages.INFO, 'erro ao revalidar')
                    # print('erro ao revalidar')

                    return JsonResponse({
                        'mensagem': 'erro ao revalidar',
                        'id': self.object.pk,
                        'status': 'fail'
                    })

            if lock_delete_form_id in request.POST and documento_lock.bloqueado_por.pk == request.user.pk:
                if delete_form.is_valid():
                    with transaction.atomic():
                        documento_lock.delete()
                    # messages.add_message(request, messages.INFO, 'deletado com sucesso')
                    # print('deletado com sucesso')
                    return JsonResponse({
                        'mensagem': 'deletado com sucesso',
                        'id': self.object.pk,
                        'status': 'success'
                    })
                else:
                    # messages.add_message(request, messages.INFO, 'erro ao deletar')
                    # print('erro ao deletar')
                    return JsonResponse({
                        'mensagem': 'erro ao deletar',
                        'id': self.object.pk,
                        'status': 'fail'
                    })

                    # return JsonResponse({
                    #     'mensagem': 'post_invalido',
                    #     'id': model_instance.pk,
                    #     'status': 'fail'
                    # })
        return original_response


class EditarView(LuzfcbLockMixin, generic.UpdateView):
    template_name = 'app_test/person_update.html'
    model = Person
    fields = ('nome',)

