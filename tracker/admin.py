from django.contrib import admin
from .models import People, Project, Issue, ProjectModification, IssueModification

# Register your models here.
class IssueAdmin(admin.ModelAdmin):
  list_display = ('summary', 'resolved', 'created_on', 'created_by')

  def save_model(self, request, obj, form, change):
    obj.created_by = request.user
    super().save_model(request, obj, form, change) 
    
class ProjectAdmin(admin.ModelAdmin):
  list_display = ('project_name', 'created_on', 'created_by')

  def save_model(self, request, obj, form, change):
    obj.created_by = request.user
    super().save_model(request, obj, form, change) 

admin.site.register(People)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectModification)
admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueModification)
