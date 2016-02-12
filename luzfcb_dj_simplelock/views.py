import logging

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .models import ObjectLock
from .utils import get_label
from sample_project.app_test.models import Person

###################################################################################################################
lock_expire_time_in_seconds = 30
lock_revalidated_at_every_x_seconds = 5
lock_revalidate_form_id = 'id_revalidar_form'
lock_delete_form_id = 'id_deletar_form'
lock_this_view_named_url_str = ''
update_view_str = 'person:editar'
detail_view_str = 'person:detail'

# Get an instance of a logger
logger = logging.getLogger(__name__)


def editar(request, pk):
    # obter model para editar
    model_instance = get_object_or_404(Person, pk=pk)
    if request.method == 'GET':
        # verificar se nao ha bloqueio
        # se nao houver bloqueio, dar permissao de edicao exclusiva para o usuario da requisicao

        # try:
        label = get_label(model_instance)
        now_time = timezone.now()
        next_expire_time = now_time + timezone.timedelta(seconds=lock_expire_time_in_seconds)

        updated_values = {'model_pk': model_instance.pk,
                          'app_and_model': label,
                          'bloqueado_por': request.user,
                          'bloqueado_por_user_name': request.user.username,
                          'bloqueado_por_full_name': request.user.get_full_name(),
                          # session_key: session.session_key,
                          'expire_date': next_expire_time}
        with transaction.atomic():
            documento_lock, created = ObjectLock.objects.get_or_create(defaults=updated_values,
                                                                       app_and_model=label,
                                                                       model_pk=model_instance.pk)
            if documento_lock and now_time > documento_lock.expire_date:
                documento_lock.bloqueado_por = updated_values['bloqueado_por']
                documento_lock.bloqueado_por_user_name = updated_values['bloqueado_por_user_name']
                documento_lock.bloqueado_por_full_name = updated_values['bloqueado_por_full_name']
                documento_lock.save()

            # documento_lock, created = ObjectLock.objects.update_or_create(defaults=updated_values,
            #                                                      app_and_model=label,
            #                                                      model_pk=model_instance.pk)
            if not created and not documento_lock.bloqueado_por.pk == request.user.pk:
                detail_url = reverse(detail_view_str, kwargs={'pk': model_instance.pk})
                msg = 'Documento está sendo editado por {} - Disponivel somente para visualização'.format(
                    documento_lock.bloqueado_por_full_name or documento_lock.bloqueado_por_user_name)
                messages.add_message(request, messages.INFO, msg)
                logger.debug(msg)
                print(msg)
                return redirect(detail_url, permanent=False)

    else:
        pass
    return render(request, 'app_test/person_update.html', context={
        'object': model_instance,
        'update_view_str': update_view_str,
        'deletar_form_id': lock_delete_form_id,
        'revalidar_form_id': lock_revalidate_form_id,
        'revalidate_lock_at_every_x_seconds': lock_revalidated_at_every_x_seconds}
                  )


def atualizar_ou_criar_bloqueio(request, model_instance):
    pass

# def remover_bloqueio(request, model_instance):
#     pass
#
#     obj = get_object_or_404(Person, pk=pk)
#
#     if request.method == 'POST':
#         pass
#     else:
#         # GET
#         if obj:
#             try:
#                 label = get_label(obj)
#                 documento_lock = ObjectLock.objects.get(model_pk=obj.pk, app_and_model=label)
#                 agora = timezone.now()
#                 if documento_lock and agora > documento_lock.expire_date:
#                     delete_lock(request, obj, agora)
#                     # notificar o usuario ObjectLock.bloqueado_por que ele perdeu o bloqueio
#                     #
#                     # trocar por um update
#                     update_lock(request, obj)
#                     return ''  # original_response
#
#                 if documento_lock and not documento_lock.bloqueado_por.pk == request.user.pk:
#                     detail_url = reverse('pessoa:detail', kwargs={'pk': obj.pk})
#                     msg = 'Documento está sendo editado por {} - Disponivel somente para visualização'.format(
#                         documento_lock.bloqueado_por_full_name or documento_lock.bloqueado_por_user_name)
#                     messages.add_message(request, messages.INFO, msg)
#                     logger.debug(msg)
#                     print(msg)
#                     return redirect(detail_url, permanent=False)
#             except ObjectLock.DoesNotExist:
#                 create_lock(request, obj)
#
#         revalidar_form = ReValidarForm(prefix='revalidar', initial={'hash': obj.pk, 'id': obj.pk})
#         deletar_form = DeletarForm(prefix='deletar', initial={'hash': obj.pk, 'id': obj.pk})
#
#         revalidate = None
#         context = {}
#
#         if lock_revalidated_at_every_x_seconds and lock_revalidated_at_every_x_seconds <= lock_expire_time_in_seconds / 2:
#             revalidate = lock_revalidated_at_every_x_seconds
#
#         context.update(
#             {
#                 'revalidate_lock_at_every_x_seconds': revalidate,
#                 'revalidar_form': revalidar_form,
#                 'revalidar_form_id': lock_revalidate_form_id,
#                 'deletar_form': deletar_form,
#                 'deletar_form_id': lock_delete_form_id,
#                 'update_view_str': update_view_str,
#                 'object': obj,
#
#             }
#         )
#
#         return render(request, 'core/pessoa_update.html', context=context)
#
