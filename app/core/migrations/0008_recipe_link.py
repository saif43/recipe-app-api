# Generated by Django 2.2.16 on 2020-09-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='link',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
