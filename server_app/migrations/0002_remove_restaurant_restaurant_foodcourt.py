# Generated by Django 4.1.3 on 2022-11-15 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("server_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="restaurant",
            name="restaurant_foodcourt",
        ),
    ]
