from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView)
from .models import People, Project, Issue, SoftDeleteQuerySet
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd

class IndexView(ListView):
    model = Project
    template_name = 'index.html'
    queryset = Project.objects.all()

    def get_context_data(self, **kwargs):
        projects = Project.objects.all()
        people = People.objects.all()
        people_active = People.objects.only_active()
        issues = Issue.objects.all()
        issues_active = Issue.objects.all().filter(actual_resolution=None)
        issues_solved = len(issues) - len(issues_active)
        context = super(IndexView, self).get_context_data(**kwargs)

        data = [len(issues_active), issues_solved]
        labels = ['Open', 'Solved']
        issues_graphs = []
        issues_graphs.append(
            go.Pie(values=data, labels=labels)
        )

        # Getting HTML needed to render the plot.
        issues_plot_div = plot({'data': issues_graphs}, output_type='div')

        projects_data = pd.DataFrame()
        for i in issues:
            row = pd.DataFrame({'Project': i.related_project.project_name, 'Solver': i.assigned_to, 'Priority': i.priority, 'Item': 1}, index=[0])
            projects_data = pd.concat([row,projects_data.loc[:]]).reset_index(drop=True)        

        projects_graphs = []
        projects_graphs.append(
            go.Pie(values=projects_data['Item'], labels=projects_data['Project'])
        )

        # Getting HTML needed to render the plot.
        projects_plot_div = plot({'data': projects_graphs}, output_type='div')

        context['projects'] = projects
        context['people'] = people
        context['people_active'] = people_active
        context['issues'] = issues
        context['issues_active'] = issues_active
        context['issues_solved'] = issues_solved
        context['issues_plot_div'] = issues_plot_div
        context['projects_plot_div'] = projects_plot_div
        return context

@login_required
def people(request):
    return render(request, 'people/people.html')
