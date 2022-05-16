from django.contrib import admin
from .models import People, Project, Issue

# Register your models here.
class IssueAdmin(admin.ModelAdmin):
  list_display = ('summary', 'resolved', 'created_on')

admin.site.register(People)
admin.site.register(Project)
admin.site.register(Issue, IssueAdmin)
