from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')


@login_required
def people(request):
    return render(request, 'people.html')
