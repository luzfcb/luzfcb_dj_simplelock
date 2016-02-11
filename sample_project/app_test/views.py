from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .models import Person
from .forms import PersonForm


class PersonList(generic.ListView):
    model = Person
    template_name = 'luzfcb_dj_simplelock/pessoa_list.html'


class PersonDetail(generic.DetailView):
    model = Person
    template_name = 'luzfcb_dj_simplelock/pessoa_detail.html'


class PersonCreate(generic.CreateView):
    model = Person
    form_class = PersonForm
    prefix = 'pessoa_create'
    template_name = 'luzfcb_dj_simplelock/pessoa_create.html'

    def get_success_url(self):
        return reverse_lazy('pessoa:update', kwargs={'pk': self.object.pk})
