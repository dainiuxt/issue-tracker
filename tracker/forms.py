from .models import Project, Issue
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name',
            'start_date',
            'target_end',
            'actual_end',
            'assigned_to']
        widgets = {
            'start_date': DateInput(),
            'target_end': DateInput(),
            'actual_end': DateInput(),
            'created_on': forms.HiddenInput(),
            'created_by': forms.HiddenInput()
        }

class IssueCreateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'identified_by',
            'assigned_to',
            'summary',
            'description',
            # 'identification_date',
            # 'related_project',
            'priority',
            'target_resolution',
            'progress',
            'actual_resolution',
            'res_summary']
        widgets = {
            # 'identification_date': DateInput(),
            'target_resolution': DateInput(),
            'actual_resolution': DateInput(),
            'created_on': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
            'related_project': forms.HiddenInput(),
        }
