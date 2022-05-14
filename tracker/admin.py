from django.contrib import admin
from .models import People, Project, Issue

# Register your models here.

admin.site.register(People)
admin.site.register(Project)
admin.site.register(Issue)
