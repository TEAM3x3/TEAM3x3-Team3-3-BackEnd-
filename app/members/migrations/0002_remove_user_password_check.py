# Generated by Django 3.1 on 2020-08-19 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password_check',
        ),
    ]
