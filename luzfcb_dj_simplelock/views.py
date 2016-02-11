from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import ObjectLock
from .utils import get_label
from app_test.models import Person


def editar(request, pk):
    # obter model para editar
    model_instance = get_object_or_404(Person, pk=pk)
    if request.method == 'GET':
        # verificar se nao ha bloqueio
        # se nao houver bloqueio, dar permissao de edicao exclusiva para o usuario da requisicao
        #

        pass
    else:
        pass
    return render(request, 'luzfcb_dj_simplelock/pessoa_update.html')


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
