from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
  project_name = models.CharField('Project name', max_length=200)
  start_date = models.DateField('Start date')
  target_end = models.DateField('Target end date')
  actual_end = models.DateField('Actual end date', null=True, blank=True)
  created_on = models.DateField('Creation date')
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='project_creator')
  modified_on = models.DateField('Change date', null=True, blank=True)
  modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.project_name


class People(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  assigned_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
  created_on = models.DateField('Creation date')
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='createdby')
  modified_on = models.DateField('Change date', null=True, blank=True)
  modified_by = models.ManyToManyField(User, related_name='modifiedby', blank=True)

  def __str__(self):
    return self.user.username

  class Meta:
    verbose_name = 'People'
    verbose_name_plural = 'People'

class Issue(models.Model):
  summary = models.CharField('Issue summary', max_length=255)
  description = models.TextField('Description', null=True)
  identified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  identification_date = models.DateField('Identified on')
  related_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
  assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issue_solver', blank=True)

  STATUS_LIST = (
    ('o', 'Open'),
    ('c', 'Closed'),
  )

  status = models.CharField('Status', max_length=1, default='o', choices=STATUS_LIST)

  PIORITY_LIST = (
    ('l', 'Low'),
    ('m', 'Medium'),
    ('h', 'High'),
    ('e', 'Extra'),
  )

  priority = models.CharField('Priority', default='m', max_length=1, choices=PIORITY_LIST)
  target_resolution = models.DateField('Planned resolution')
  progress = models.TextField('Progress', null=True)
  actual_resolution = models.DateField('Actual resolution', null=True, blank=True)
  res_summary = models.TextField('Resolution summary', null=True, blank=True)
  created_on = models.DateField('Creation date')
  created_by = models.ManyToManyField(User, related_name='issue_owner')
  modified_on = models.DateField('Change date', null=True, blank=True)
  modified_by = models.ManyToManyField(User, related_name='issue_modifier', blank=True)

  def __str__(self):
    return self.summary

  @property
  def status(self):
    if self.actual_resolution is None:
      self.status = 'o'
    else:
      self.status = 'c'
    return self.status
