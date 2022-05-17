# Generated by Django 4.0.4 on 2022-05-17 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0021_project_assigned_to_delete_assignedprojects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
