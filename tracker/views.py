from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, DetailView)
from .models import People, Project, Issue
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd

projects = Project.objects.all()
people = People.objects.all()
people_active = People.objects.only_active()
issues = Issue.objects.all()
issues_active = Issue.objects.all().filter(actual_resolution=None)
issues_solved = []
for i in issues:
    if i.actual_resolution != None:
        issues_solved.append(i)

data = [len(issues_active), len(issues_solved)]
labels = ['Open', 'Solved']
issues_graphs = []
issues_graphs.append(
    go.Pie(values=data, labels=labels)
)
# Getting HTML needed to render the plot.
issues_status_div = plot({'data': issues_graphs}, output_type='div')

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

class IndexView(ListView):
    model = Project
    template_name = 'index.html'
    queryset = Project.objects.all()

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)
        context['projects'] = projects
        context['people'] = people
        context['people_active'] = people_active
        context['issues'] = issues
        context['issues_active'] = issues_active
        context['issues_solved'] = issues_solved
        context['issues_status_div'] = issues_status_div
        context['projects_plot_div'] = projects_plot_div
        context['index_menu_active'] = 'active'
        return context

class ProjectsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/projects.html'

    def get_context_data(self, **kwargs):

        projects_data = pd.DataFrame()
        for i in issues_active:
            row = pd.DataFrame({'Project': i.related_project.project_name, 'Solver': i.assigned_to, 'Priority': i.get_priority_display(), 'Item': 1}, index=[0])
            projects_data = pd.concat([row,projects_data.loc[:]]).reset_index(drop=True)        
        projects_graphs = []
        projects_graphs.append(
            go.Pie(values=projects_data['Item'], labels=projects_data['Priority'])
        )
        # Getting HTML needed to render the plot.
        plot_div = plot({'data': projects_graphs}, output_type='div')

        context = super(ProjectsView, self).get_context_data(**kwargs)
        context['projects_menu_active'] = 'active'
        context['projects'] = projects
        context['issues'] = issues
        context['issues_active'] = issues_active
        context['issues_solved'] = issues_solved
        context['plot_div'] = plot_div
        return context


class IssuesView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'issues/issues.html'

    def get_context_data(self, **kwargs):

        issues_data = pd.DataFrame()
        for i in issues_active:
            row = pd.DataFrame({'Project': i.related_project.project_name, 'Solver': i.assigned_to, 'Priority': i.get_priority_display(), 'Item': 1}, index=[0])
            issues_data = pd.concat([row,issues_data.loc[:]]).reset_index(drop=True)        
        issues_graphs = []
        issues_graphs.append(
            go.Pie(values=issues_data['Item'], labels=issues_data['Priority'])
        )
        # Getting HTML needed to render the plot.
        plot_div = plot({'data': issues_graphs}, output_type='div')

        issues_by_project = []
        issues_by_project.append(
            go.Pie(values=issues_data['Item'], labels=issues_data['Project'])
        )
        # Getting HTML needed to render the plot.
        issues_by_proj_div = plot({'data': issues_by_project}, output_type='div')

        context = super(IssuesView, self).get_context_data(**kwargs)
        context['issues_menu_active'] = 'active'
        context['issues'] = issues
        context['issues_active'] = issues_active
        context['issues_solved'] = issues_solved
        context['plot_div'] = plot_div
        context['issues_by_proj_div'] = issues_by_proj_div
        return context

class ProfileView(ListView, LoginRequiredMixin):
    model = People
    template_name = 'people/people.html'
    queryset = People.objects.all()

    def get_context_data(self, **kwargs):

        people = People.objects.all()
        # user = People.objects.all().filter(pk=request.user.id)
        projects = Project.objects.all().filter(assigned_to=self.request.user.id)
        people_active = People.objects.only_active()
        issues = Issue.objects.all()
        issues_active = Issue.objects.all().filter(actual_resolution=None)
        issues_solved = []
        for i in issues:
            if i.actual_resolution != None:
                issues_solved.append(i)

        context = super(ProfileView, self).get_context_data(**kwargs)
        context['projects'] = projects
        context['people'] = people
        context['people_active'] = people_active
        context['issues'] = issues
        context['issues_active'] = issues_active
        context['issues_solved'] = issues_solved
        context['issues_status_div'] = issues_status_div
        context['projects_plot_div'] = projects_plot_div
        context['people_menu_active'] = 'active'
        return context
