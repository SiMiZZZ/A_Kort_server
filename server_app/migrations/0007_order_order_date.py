# Generated by Django 4.1.3 on 2022-11-24 09:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("server_app", "0006_order_order_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_date",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
