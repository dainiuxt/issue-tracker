# Generated by Django 4.0.4 on 2022-05-16 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_alter_issue_created_on_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='resolved',
        ),
    ]
