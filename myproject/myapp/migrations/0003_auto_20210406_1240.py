# Generated by Django 3.1.7 on 2021-04-06 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20210406_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='picture',
            field=models.ImageField(blank=True, default='logo.jpg', upload_to=''),
        ),
    ]
