# Generated by Django 2.2.15 on 2020-09-05 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='user',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
