# Generated by Django 4.0.4 on 2022-05-16 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_issue_resolved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='resolved',
        ),
    ]
