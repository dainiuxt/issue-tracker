from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import People, Project, Issue, SoftDeleteQuerySet

def index(request):
    projects = Project.objects.all()
    people = People.objects.all()
    people_active = People.objects.only_active()
    issues = Issue.objects.all()

    context = {
        'projects': projects,
        'people': people,
        'people_active': people_active,
        'issues': issues
    }
    return render(request, 'index.html', context=context)


@login_required
def people(request):
    return render(request, 'people.html')
