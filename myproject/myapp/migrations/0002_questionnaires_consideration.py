# Generated by Django 3.1.7 on 2021-03-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaires',
            name='consideration',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]