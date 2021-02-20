from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.generic import FormView

from .models import PersonSet, Person
from .forms import CreateDeckForm
from django.contrib import messages
from django.urls import reverse
from django.views.generic.detail import DetailView


def index(request, hash):
    personset = PersonSet.objects.filter(hash=hash).first()
    images = personset.person_set.all()
    return render(request, 'main.html', {"images": images})


def decks(request):
    decks = PersonSet.objects.all()  # filter(user_id=request.user.id)
    return render(request, 'decks.html', {"decks": decks})


class DeckView(FormView):
    form_class = CreateDeckForm
    template_name = 'create_deck.html'  # Replace with your template.
    success_url = '/decks'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('images')
        if form.is_valid():
            set = PersonSet(name=form.data.get("name"), user_id=request.user.id)
            set.save()
            for file in files:
                instance = Person(photo=file, name=file.name.split('.')[0], person_set=set)  # match the model.
                instance.save()
            set.save()
            DeckView.success_url = reverse('index', kwargs={'hash': set.hash})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
# def deck(request, hash):
# deck = PersonSet.objects.get(hash=hash)
# return render(request, 'deck.html', {"deck": deck})
