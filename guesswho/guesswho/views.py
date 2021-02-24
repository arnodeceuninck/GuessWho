from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.generic import FormView

from .models import PersonSet, Person, Settings
from .forms import CreateDeckForm
from django.contrib import messages
from django.urls import reverse
from django.views.generic.detail import DetailView
import string
import random


def home(request):
    return redirect("index", hash=Settings.objects.first().hash)

def index(request, hash):
    personset = PersonSet.objects.filter(pk=hash).first()
    if not personset:
        raise Http404
    # images = personset.person_set.all()
    print(len(personset.person_set.all()))
    return render(request, 'main.html', {"deck": personset})

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_uppercase + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

@login_required
def decks(request):
    if request.method == 'POST':
        form = CreateDeckForm(request.POST, request.FILES)
        if form.is_valid():

            hash = get_random_alphanumeric_string(5)
            while PersonSet.objects.filter(hash=hash).count():
                hash = get_random_alphanumeric_string(5)

            person_set = PersonSet(name=form.data.get("name"), user_id=request.user.id, hash=hash)
            person_set.save()
            files = request.FILES.getlist('images')
            for file in files:
                instance = Person(photo=file, name=file.name.split('.')[0], person_set=person_set)  # match the model.
                instance.save()
            person_set.save()
            return HttpResponseRedirect(reverse('index', kwargs={'hash': person_set.hash}))
    else:
        form = CreateDeckForm()
    person_decks = PersonSet.objects.filter(user_id=request.user.id)
    for deck in person_decks:
        print(deck.name)
    return render(request, 'decks.html', {"decks": person_decks, "create_form": form})
