# Generated by Django 3.1.7 on 2021-04-06 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210406_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='picture',
            field=models.ImageField(blank=True, default='C:\\Users\\Denys\\Desktop\\python_thesis\\myproject\\logo.jpg', upload_to=''),
        ),
    ]
