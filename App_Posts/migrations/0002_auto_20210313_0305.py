# Generated by Django 3.1.5 on 2021-03-12 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-upload_date']},
        ),
    ]
