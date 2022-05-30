from django.urls import path
from . import views
from tracker.views import (IndexView,
                            ProjectsView,
                            ProjectView,
                            ProjectCreateView,
                            IssuesView,
                            IssueCreateView,
                            ProfileView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('people/', ProfileView.as_view(), name='people'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/new', ProjectCreateView.as_view(), name='new-project'),
    path('projects/<int:pk>/', ProjectView.as_view(), name='project'),
    path('issues/', IssuesView.as_view(), name='issues'),
    path('issues/new', IssueCreateView.as_view(), name='new-issue'),
]
