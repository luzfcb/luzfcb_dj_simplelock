from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic

from luzfcb_dj_simplelock.views import LuzfcbLockMixin

from .forms import PersonForm
from .models import Person


class PersonList(generic.ListView):
    model = Person
    template_name = 'app_test/person_list.html'


class PersonDetail(generic.DetailView):
    model = Person
    template_name = 'app_test/person_detail.html'


class PersonCreate(generic.CreateView):
    model = Person
    form_class = PersonForm
    prefix = 'person_create'
    template_name = 'app_test/person_create.html'

    def get_success_url(self):
        return reverse_lazy('person:editar', kwargs={'pk': self.object.pk})


class EditarView(LuzfcbLockMixin, generic.UpdateView):
    template_name = 'app_test/person_update.html'
    model = Person
    prefix = 'person_prefix'
    fields = ('nome',)
    form_id = 'id_person_update_form_submit'
    lock_this_view_url = None
    # update_view_named_url = 'person:editar'

    def get_success_url(self):
        return reverse('person:editar', kwargs={'pk': self.object.pk})

    def get_lock_url_to_redirect_if_locked(self):
        return reverse('person:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EditarView, self).get_context_data(**kwargs)
        send_ajax_post = self.request.GET.get('ajax', None)
        context.update({
            'send_ajax_post': send_ajax_post if send_ajax_post else False
        })
        return context

    def form_valid(self, form):
        if self.form_id in self.request.POST:
            return super(EditarView, self).form_valid(form)
        else:
            a = {}  # NOQA
            return self.render_to_response(context=self.get_context_data(**a))


DEFAULT_LOCK_EXPIRE_TIME_IN_SECONDS = 1
DEFAULT_LOCK_REVALIDATED_AT_EVERY_X_SECONDS = 1
DEFAULT_LOCK_REVALIDATE_FORM_ID = 'id_revalidar_form'
DEFAULT_LOCK_REVALIDATE_FORM_PREFIX = 'revalidar'
DEFAULT_LOCK_DELETE_FORM_ID = 'id_deletar_form'
DEFAULT_LOCK_DELETE_FORM_PREFIX = 'deletar'


class EditarView2(EditarView):
    lock_expire_time_in_seconds = DEFAULT_LOCK_EXPIRE_TIME_IN_SECONDS
    lock_revalidated_at_every_x_seconds = DEFAULT_LOCK_REVALIDATED_AT_EVERY_X_SECONDS
    lock_revalidate_form_id = DEFAULT_LOCK_REVALIDATE_FORM_ID
    lock_revalidate_form_prefix = DEFAULT_LOCK_REVALIDATE_FORM_PREFIX
    lock_delete_form_id = DEFAULT_LOCK_DELETE_FORM_ID
    lock_delete_form_prefix = DEFAULT_LOCK_DELETE_FORM_PREFIX
