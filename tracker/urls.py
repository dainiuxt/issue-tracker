from django.urls import path
from django.conf.urls import handler403
from . import views
from tracker.views import (IndexView,
                            ProjectsView,
                            ProjectView,
                            ProjectCreateView,
                            IssuesView,
                            IssueView,
                            IssueCreateView,
                            IssueUpdateView,
                            ProfileView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('people/', ProfileView.as_view(), name='people'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/new/', ProjectCreateView.as_view(), name='new-project'),
    path('projects/<int:pk>/', ProjectView.as_view(), name='project'),
    path('issues/', IssuesView.as_view(), name='issues'),
    path('issues/<int:pk>/', IssueView.as_view(), name='issue'),
    path('issues/<int:pk>/edit/', IssueUpdateView.as_view(), name='edit-issue'),
    path('projects/<int:pk>/newissue/', IssueCreateView.as_view(), name='new-issue'),
]
