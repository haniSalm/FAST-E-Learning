# Generated by Django 4.2 on 2024-12-03 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0013_coursematerial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.TextField(blank=True, default='No Description'),
            preserve_default=False,
        ),
    ]