# Generated by Django 4.0.4 on 2022-05-16 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_remove_issue_resolved'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='resolved',
            field=models.BooleanField(default=False, verbose_name='Status'),
        ),
    ]