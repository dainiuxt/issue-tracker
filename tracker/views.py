from distutils.log import error
from django.shortcuts import render, reverse
from django.views.generic import (ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView)
from .models import People, Project, Issue
from .forms import ProjectCreateForm, IssueCreateForm
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib import messages
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from django.urls import reverse_lazy


def custom_error_403(request, exception):
    return render(request, 'err/403.html', {})

projects = Project.objects.all()
people = People.objects.all()
people_active = People.objects.only_active()
issues = Issue.objects.all()
issues_active = Issue.objects.all().filter(actual_resolution=None)
issues_solved = []
for i in issues:
    if i.actual_resolution != None:
        issues_solved.append(i)

def issues_chart_main():
    data = [len(issues_active), len(issues_solved)]
    labels = ['Open', 'Solved']
    issues_graphs = []
    issues_graphs.append(
        go.Pie(values=data, labels=labels)
    )
    # Getting HTML needed to render the plot.
    div = plot({'data': issues_graphs}, output_type='div')
    return div

def issues_chart(data, labels):
    issues_act = issues_active
    issues_data = pd.DataFrame()
    for i in issues_act:
        row = pd.DataFrame({'Project': i.related_project.project_name, 'Solver': i.assigned_to, 'Priority': i.get_priority_display(), 'Item': 1}, index=[0])
        issues_data = pd.concat([row,issues_data.loc[:]]).reset_index(drop=True)          
    projects_graphs = []
    projects_graphs.append(
        go.Pie(values=issues_data[data], labels=issues_data[labels])
    )
    # Getting HTML needed to render the plot.
    div = plot({'data': projects_graphs}, output_type='div')
    return div

def projects_chart(data, labels):
    projects_data = pd.DataFrame()
    for i in issues:
        row = pd.DataFrame({'Project': i.related_project.project_name, 'Solver': i.assigned_to, 'Priority': i.get_priority_display(), 'Item': 1}, index=[0])
        projects_data = pd.concat([row,projects_data.loc[:]]).reset_index(drop=True)        
    projects_graphs = []
    projects_graphs.append(
        go.Pie(values=projects_data[data], labels=projects_data[labels])
    )
    # Getting HTML needed to render the plot.
    div = plot({'data': projects_graphs}, output_type='div')
    return div

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
        issues_solved = []
        for i in issues:
            if i.actual_resolution != None:
                issues_solved.append(i)

        issues_status_div = issues_chart_main()
        projects_plot_div = projects_chart('Item', 'Project')
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
        context = super(ProjectsView, self).get_context_data(**kwargs)
        context['projects_menu_active'] = 'active'
        context['projects'] = projects
        context['issues'] = issues
        return context

class ProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project.html'

    def get_success_url(self):
        return reverse('project', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        projects = Project.objects.all()
        issues = Issue.objects.all()
        issues_active = Issue.objects.all().filter(actual_resolution=None)
        issues_solved = []
        for i in issues:
            if i.actual_resolution != None:
                issues_solved.append(i)
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['projects_menu_active'] = 'active'
        context['projects'] = projects
        context['issues'] = issues
        context['issues_active'] = issues_active
        context['issues_solved'] = issues_solved
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm

    success_url = reverse_lazy('index')
    template_name = 'projects/new_project.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.date = date.today()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class IssuesView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'issues/issues.html'

    def get_context_data(self, **kwargs):
        projects = Project.objects.all()
        issues = Issue.objects.all()
        issues_active = Issue.objects.all().filter(actual_resolution=None)
        issues_solved = []
        for i in issues:
            if i.actual_resolution != None:
                issues_solved.append(i)
        context = super(IssuesView, self).get_context_data(**kwargs)
        context['issues_menu_active'] = 'active'
        context['issues'] = issues
        context['issues_active'] = issues_active
        context['issues_solved'] = issues_solved
        context['projects'] = projects
        return context


class IssueView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'issues/issue.html'

    def get_success_url(self):
        return reverse('issue', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        projects = Project.objects.all()
        issues = Issue.objects.all()
        context = super(IssueView, self).get_context_data(**kwargs)
        context['issues_menu_active'] = 'active'
        context['projects'] = projects
        context['issues'] = issues
        return context

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueCreateForm

    success_url = reverse_lazy('index')
    template_name = 'issues/new_issue.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.related_project = Project.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        project_id = Project.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        context['project_id'] = project_id
        return context

class IssueUpdateView(UserPassesTestMixin,
                    LoginRequiredMixin,
                    UpdateView):
    model = Issue
    form_class = IssueCreateForm
    
    success_url = reverse_lazy('index')
    template_name = 'issues/new_issue.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        issue = self.get_object()
        if self.request.user == issue.assigned_to or self.request.user == issue.created_by:
            return True
        return False


class ProfileView(ListView, LoginRequiredMixin):
    model = People
    template_name = 'people/people.html'
    queryset = People.objects.all()

    def get_context_data(self, **kwargs):

        projects = Project.objects.all().filter(assigned_to=self.request.user.id)
        issues_status_div = issues_chart('Item', 'Priority')
        projects_plot_div = projects_chart('Item', 'Priority')
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
