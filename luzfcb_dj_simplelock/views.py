# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone

from .forms import DeleteForm, ReValidateForm
from .models import ObjectLock
from .utils import get_label

###################################################################################################################
# Get an instance of a logger
logger = logging.getLogger(__name__)  # pylint:disable=invalid-name

DEFAULT_LOCK_EXPIRE_TIME_IN_SECONDS = 30
DEFAULT_LOCK_REVALIDATED_AT_EVERY_X_SECONDS = 20
DEFAULT_LOCK_REVALIDATE_FORM_ID = 'id_revalidar_form'
DEFAULT_LOCK_REVALIDATE_FORM_PREFIX = 'revalidar'
DEFAULT_LOCK_DELETE_FORM_ID = 'id_deletar_form'
DEFAULT_LOCK_DELETE_FORM_PREFIX = 'deletar'


def revalidate_lock(documento_lock, updated_values_dict):
    documento_lock.bloqueado_por = updated_values_dict['bloqueado_por']
    documento_lock.bloqueado_por_user_name = updated_values_dict['bloqueado_por_user_name']
    documento_lock.bloqueado_por_full_name = updated_values_dict['bloqueado_por_full_name']
    documento_lock.expire_date = updated_values_dict['expire_date']
    with transaction.atomic():
        documento_lock.save()


class LuzfcbLockMixin(object):

    lock_expire_time_in_seconds = None
    lock_revalidated_at_every_x_seconds = None  # pylint:disable=invalid-name
    lock_revalidate_form_id = None
    lock_revalidate_form_prefix = None
    lock_delete_form_id = None
    lock_delete_form_prefix = None
    lock_use_builtin_jquery = True
    lock_use_builtin_jquery_csrftoken = True  # pylint:disable=invalid-name
    lock_url_to_redirect_if_locked = None  # pylint:disable=invalid-name
    lock_this_view_url = None

    def get_lock_expire_time_in_seconds(self):  # pylint:disable=invalid-name
        if not self.lock_expire_time_in_seconds:
            return DEFAULT_LOCK_EXPIRE_TIME_IN_SECONDS
        if self.lock_expire_time_in_seconds < 1:
            raise ImproperlyConfigured(
                '{0} requires the "lock_expire_time_in_seconds" attribute must be a positive integer'
                ''.format(self.__class__.__name__))
        return self.lock_expire_time_in_seconds

    def get_lock_revalidated_at_every_x_seconds(self):  # pylint:disable=invalid-name
        if not self.lock_revalidated_at_every_x_seconds:
            return DEFAULT_LOCK_REVALIDATED_AT_EVERY_X_SECONDS
        if self.lock_revalidated_at_every_x_seconds > self.get_lock_expire_time_in_seconds():
            raise ImproperlyConfigured(
                '{0} "lock_revalidated_at_every_x_seconds" attribute should be less than "lock_expire_time_in_seconds"'
                ''.format(self.__class__.__name__))
        return self.lock_revalidated_at_every_x_seconds

    def get_lock_revalidate_form_id(self):
        if not self.lock_revalidate_form_id:
            return DEFAULT_LOCK_REVALIDATE_FORM_ID
        return self.lock_revalidate_form_id

    def get_lock_revalidate_form_prefix(self):
        if not self.lock_revalidate_form_prefix:
            return DEFAULT_LOCK_REVALIDATE_FORM_PREFIX
        return self.lock_revalidate_form_prefix

    def get_lock_delete_form_id(self):
        if not self.lock_delete_form_id:
            return DEFAULT_LOCK_DELETE_FORM_ID
        return self.lock_delete_form_id

    def get_lock_delete_form_prefix(self):
        if not self.lock_delete_form_prefix:
            return DEFAULT_LOCK_DELETE_FORM_PREFIX
        return self.lock_delete_form_prefix

    def get_lock_this_view_url(self):
        # if self.update_view_named_url is None:
        #     raise ImproperlyConfigured(
        #         '{0} requires the "update_view_named_url" attribute to be '
        #         'set.'.format(self.__class__.__name__))
        return self.lock_this_view_url

    def get_lock_url_to_redirect_if_locked(self):  # pylint:disable=invalid-name
        if self.lock_url_to_redirect_if_locked is None:
            raise ImproperlyConfigured(
                '{0} is missing the '
                'lock_redirect_to_url_if_locked. Define {0}.lock_redirect_to_url_if_locked or '
                'override {0}.get_lock_url_to_redirect_if_locked().'.format(
                    self.__class__.__name__))
        return self.lock_url_to_redirect_if_locked

    def get_context_data(self, **kwargs):
        context = super(LuzfcbLockMixin, self).get_context_data(**kwargs)

        revalidate_form = ReValidateForm(prefix=self.get_lock_revalidate_form_prefix(),
                                         initial={'hashe': self.object.pk, 'idd': self.object.pk})
        delete_form = DeleteForm(prefix=self.get_lock_delete_form_prefix(),
                                 initial={'hashe': self.object.pk, 'idd': self.object.pk})

        context.update(
            {
                'update_view_str': self.get_lock_this_view_url(),
                'delete_form_id': self.get_lock_delete_form_id(),
                'delete_form': delete_form,
                'revalidate_form': revalidate_form,
                'revalidate_form_id': self.get_lock_revalidate_form_id(),
                'revalidate_lock_at_every_x_seconds': self.get_lock_revalidated_at_every_x_seconds(),
                'lock_use_builtin_jquery': self.lock_use_builtin_jquery,
                'lock_use_builtin_jquery_csrftoken': self.lock_use_builtin_jquery_csrftoken
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        original_response = super(LuzfcbLockMixin, self).get(request, *args, **kwargs)
        label = get_label(self.object)
        now_time = timezone.now()
        next_expire_time = now_time + timezone.timedelta(seconds=self.get_lock_expire_time_in_seconds())
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
                url_to_redirect_if_locked = self.get_lock_url_to_redirect_if_locked()
                msg = 'Documento está sendo editado por {} - Disponivel somente para visualização'.format(
                    documento_lock.bloqueado_por_full_name or documento_lock.bloqueado_por_user_name)
                messages.add_message(request, messages.INFO, msg)
                logger.debug(msg)
                # print(msg)
                return redirect(url_to_redirect_if_locked, permanent=False)

        return original_response

    def post(self, request, *args, **kwargs):
        if request.is_ajax and self.get_lock_revalidate_form_id() in request.POST or self.get_lock_delete_form_id() in request.POST:  # noqa
            self.object = self.get_object()
            label = get_label(self.object)
            now_time = timezone.now()
            next_expire_time = now_time + timezone.timedelta(seconds=self.get_lock_expire_time_in_seconds())
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


            revalidate_form = ReValidateForm(data=request.POST,
                                             files=request.FILES,
                                             prefix=self.get_lock_revalidate_form_prefix(),
                                             id_obj=self.object.pk)
            delete_form = DeleteForm(data=request.POST,
                                     files=request.FILES,
                                     prefix=self.get_lock_delete_form_prefix(),
                                     id_obj=self.object.pk)

            if self.get_lock_revalidate_form_id() in request.POST and documento_lock.bloqueado_por.pk == request.user.pk:  # noqa
                if revalidate_form.is_valid():
                    # se registro de bloqueio nao eh novo, e o ele ja expirou, atualiza o registro
                    # para o usuario atual da requisicao e atualiza o novo tempo de expiracao
                    if not created and documento_lock and now_time > documento_lock.expire_date:
                        revalidate_lock(documento_lock, updated_values)
                    # messages.add_message(request, messages.INFO, 'revalidado com sucesso')
                    # print('revalidado com sucesso')
                    msg = 'revalidado com sucesso'
                    logger.debug(msg)
                    return JsonResponse({
                        'mensagem': msg,
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

            if self.get_lock_delete_form_id() in request.POST and documento_lock.bloqueado_por.pk == request.user.pk:
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
        return super(LuzfcbLockMixin, self).post(request, *args, **kwargs)
