from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .models import Person
from .forms import PersonForm


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
