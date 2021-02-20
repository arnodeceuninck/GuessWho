from django.shortcuts import render
from .models import PersonSet


def index(request, hash):
    images = PersonSet.objects.get(hash=hash).person_set.all()
    return render(request, 'main.html', {"images": images})
