# Generated by Django 3.2.9 on 2021-11-30 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='seal',
            field=models.ImageField(null=True, upload_to='static/'),
        ),
    ]
