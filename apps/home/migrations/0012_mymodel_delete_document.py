# Generated by Django 4.1.1 on 2022-10-14 07:26

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0011_lifecheck_document"),
    ]

    operations = [
        migrations.CreateModel(
            name="MyModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                (
                    "health_data",
                    django_cryptography.fields.encrypt(
                        models.CharField(max_length=100)
                    ),
                ),
                (
                    "address",
                    django_cryptography.fields.encrypt(
                        models.CharField(max_length=100)
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(name="Document",),
    ]
