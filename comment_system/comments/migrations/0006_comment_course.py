# Generated by Django 4.2 on 2024-11-27 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='comments.course'),
            preserve_default=False,
        ),
    ]
