from django.urls import path
from . import views
from tracker.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('people/', views.people, name='people'),
]
