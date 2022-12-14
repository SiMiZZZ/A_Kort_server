# Generated by Django 4.1.3 on 2022-12-05 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("server_app", "0007_order_order_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user_email",
                    models.CharField(
                        default="NULL", max_length=40, verbose_name="Email"
                    ),
                ),
                (
                    "user_password_hash",
                    models.TextField(
                        default="NULL", max_length=200, verbose_name="Хэш пароля"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="order_user",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="server_app.user",
            ),
            preserve_default=False,
        ),
    ]
