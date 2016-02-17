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
    fields = ('nome',)

    update_view_str = 'person:editar'
    detail_view_str = 'person:detail'

    def get_success_url(self):
        return reverse('person:editar', kwargs={'pk': self.object.pk})
