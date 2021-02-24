import random
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CreateDeckForm
from .models import PersonSet, Person, Settings


def home(request):
    settings = Settings.objects.first()
    return redirect("index", hash=settings.hash) if settings else redirect('login')


def index(request, hash):
    personset = get_object_or_404(PersonSet, pk=hash)
    return render(request, 'main.html', {"deck": personset})

def instructions(request):
    return render(request, 'instructions.html')


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_uppercase + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


@login_required
def decks(request):
    if request.method == 'POST':
        form = CreateDeckForm(request.POST, request.FILES)
        if form.is_valid():
            person_set = add_deck_from_form(form, request)
            return HttpResponseRedirect(reverse('index', kwargs={'hash': person_set.hash}))
    else:
        form = CreateDeckForm()
    person_decks = PersonSet.objects.filter(user_id=request.user.id)
    return render(request, 'decks.html', {"decks": person_decks, "create_form": form})


def remove(request, hash):
    deck = get_object_or_404(PersonSet, pk=hash)
    if request.method == "GET":
        return render(request, 'remove.html', {"deck": deck})
    elif request.method == "POST":
        deck.delete()
        return redirect('decks')

def add_deck_from_form(form, request):
    hash = get_new_hash(6)
    person_set = PersonSet(name=form.data.get("name"), user_id=request.user.id, hash=hash)
    person_set.save()
    files = request.FILES.getlist('images')
    add_files_to_deck(files, person_set)
    return person_set


def add_files_to_deck(files, person_set):
    for file in files:
        instance = Person(photo=file, name=file.name.split('.')[0], person_set=person_set)  # match the model.
        instance.save()


def get_new_hash(length):
    hash = get_random_alphanumeric_string(length)
    while PersonSet.objects.filter(hash=hash).count():
        hash = get_random_alphanumeric_string(length)
    return hash
