# Generated by Django 4.2 on 2024-11-27 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
