# Generated by Django 4.1.1 on 2022-10-19 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0012_mymodel_delete_document"),
    ]

    operations = [
        migrations.DeleteModel(name="MyModel",),
    ]
