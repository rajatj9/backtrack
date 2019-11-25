# Generated by Django 2.2.6 on 2019-11-23 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtrack', '0003_remove_sprint_rajat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='completed',
        ),
        migrations.AddField(
            model_name='tasks',
            name='name',
            field=models.CharField(default='create', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasks',
            name='status',
            field=models.CharField(default='Not yet started', max_length=100),
            preserve_default=False,
        ),
    ]
