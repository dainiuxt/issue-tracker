from django.contrib import admin
from .models import People, Project, Issue, SoftDeleteQuerySet

class ProjectsInline(admin.TabularInline):
  model = Project
  extra = 0
  fields = ('project_name', 'start_date', 'target_end')
  list_display = ('project_name', 'start_date', 'target_end')
  readonly_fields = ['project_name']

class IssuesInline(admin.TabularInline):
  model = Issue
  extra = 0
  can_delete = False
  fields = ('summary', 'description', 'priority', 'target_resolution')
  list_display = ['summary', 'description', 'priority', 'target_resolution']


class PeopleAdmin(admin.ModelAdmin):

  list_display = ('user', 'id', 'deleted')
  readonly_fields = ['user']
  inlines = [ProjectsInline]

class IssueAdmin(admin.ModelAdmin):
  list_display = ('summary', 'resolved', 'created_on', 'created_by')

  def save_model(self, request, obj, form, change):
    obj.created_by = request.user
    super().save_model(request, obj, form, change) 

class ProjectAdmin(admin.ModelAdmin):
  list_display = ('project_name', 'created_on', 'created_by')
  inlines = [IssuesInline]

  def save_model(self, request, obj, form, change):
    obj.created_by = request.user
    super().save_model(request, obj, form, change) 

admin.site.register(People, PeopleAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
