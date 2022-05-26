from django.urls import path
from . import views
from tracker.views import (IndexView,
                            ProjectsView,
                            IssuesView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('people/', views.people, name='people'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('issues/', IssuesView.as_view(), name='issues'),
]
