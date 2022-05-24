from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import People, Project, Issue, SoftDeleteQuerySet

def index(request):
    projects = Project.objects.all()
    people = People.objects.all()
    people_active = People.objects.only_active()
    issues = Issue.objects.all()
    issues_active = Issue.objects.all().filter(actual_resolution=None)
    issues_solved = len(issues) - len(issues_active)

    context = {
        'projects': projects,
        'people': people,
        'people_active': people_active,
        'issues': issues,
        'issues_active': issues_active,
        'issues_solved': issues_solved,
    }
    return render(request, 'index.html', context=context)

@login_required
def people(request):
    return render(request, 'people.html')
