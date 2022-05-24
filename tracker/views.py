from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import People, Project, Issue, SoftDeleteQuerySet
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd


def index(request):
    projects = Project.objects.all()
    people = People.objects.all()
    people_active = People.objects.only_active()
    issues = Issue.objects.all()
    issues_active = Issue.objects.all().filter(actual_resolution=None)
    issues_solved = len(issues) - len(issues_active)

    data = [len(issues_active), issues_solved]
    labels = ['Open', 'Solved']
    issues_graphs = []
    issues_graphs.append(
        go.Pie(values=data, labels=labels)
    )

    # Setting layout of the figure.
    issues_layout = {
        #'title': 'Issues stats',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        # 'height': 420,
        # 'width': 500,
    }

    # Getting HTML needed to render the plot.
    issues_plot_div = plot({'data': issues_graphs,
                    'layout': issues_layout}, 
                    output_type='div')

    projects_data = pd.DataFrame()
    for i in issues:
        row = pd.DataFrame({'Project': i.related_project.project_name, 'Solver': i.assigned_to, 'Priority': i.priority, 'Item': 1}, index=[0])
        projects_data = pd.concat([row,projects_data.loc[:]]).reset_index(drop=True)

    projects_graphs = []
    projects_graphs.append(
        go.Pie(values=projects_data['Item'], labels=projects_data['Project'])
    )

    # Setting layout of the figure.
    projects_layout = {
        #'title': 'Issues stats',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        # 'height': 420,
        # 'width': 500,
    }

    # Getting HTML needed to render the plot.
    projects_plot_div = plot({'data': projects_graphs,
                    'layout': projects_layout}, 
                    output_type='div')

    context = {
        'projects': projects,
        'people': people,
        'people_active': people_active,
        'issues': issues,
        'issues_active': issues_active,
        'issues_solved': issues_solved,
        'issues_plot_div': issues_plot_div,
        'projects_plot_div': projects_plot_div,
    }
    return render(request, 'index.html', context=context)

@login_required
def people(request):
    return render(request, 'people.html')
