# Generated by Django 4.0.4 on 2022-05-17 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0014_alter_issueedit_modified_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issueedit',
            name='modified_on',
            field=models.DateField(auto_now_add=True, verbose_name='Change date'),
        ),
    ]
