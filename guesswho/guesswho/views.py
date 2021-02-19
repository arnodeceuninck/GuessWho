from django.shortcuts import render

def index(request):
    return render(request, 'main.html', {"images": range(18)})