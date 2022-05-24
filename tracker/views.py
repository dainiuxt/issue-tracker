from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import People, Project, Issue, SoftDeleteQuerySet
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px

def index(request):
    projects = Project.objects.all()
    people = People.objects.all()
    people_active = People.objects.only_active()
    issues = Issue.objects.all()
    issues_active = Issue.objects.all().filter(actual_resolution=None)
    issues_solved = len(issues) - len(issues_active)

    data = [len(issues_active), issues_solved]
    labels = ['Open', 'Solved']
    graphs = []
    graphs.append(
        go.Pie(values=data, labels=labels)
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Issues stats',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')

    context = {
        'projects': projects,
        'people': people,
        'people_active': people_active,
        'issues': issues,
        'issues_active': issues_active,
        'issues_solved': issues_solved,
        'plot_div': plot_div,
    }
    return render(request, 'index.html', context=context)

@login_required
def people(request):
    return render(request, 'people.html')
