# Generated by Django 2.1.3 on 2020-09-23 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cvmodel',
            old_name='interest',
            new_name='publication',
        ),
    ]
