# Generated by Django 4.1 on 2022-09-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_auto_20220907_2218"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="amka",
            field=models.CharField(db_column="amka", default="", max_length=11),
        ),
        migrations.AddField(
            model_name="patient",
            name="asfaleia",
            field=models.CharField(db_column="asfaleia", default="", max_length=45),
        ),
        migrations.AddField(
            model_name="patient",
            name="cost",
            field=models.CharField(db_column="cost", default="", max_length=45),
        ),
        migrations.AddField(
            model_name="patient",
            name="date_exam",
            field=models.CharField(db_column="date_exam", default="", max_length=45),
        ),
        migrations.AddField(
            model_name="patient",
            name="energeia",
            field=models.CharField(db_column="energeia", default="", max_length=45),
        ),
        migrations.AddField(
            model_name="patient",
            name="gnomateusi",
            field=models.CharField(db_column="gnomateusi", default="", max_length=45),
        ),
        migrations.AddField(
            model_name="patient",
            name="istoriko",
            field=models.CharField(db_column="istoriko", default="", max_length=45),
        ),
        migrations.AddField(
            model_name="patient",
            name="odigies",
            field=models.CharField(db_column="odigies", default="", max_length=45),
        ),
        migrations.AlterField(
            model_name="patient",
            name="age",
            field=models.CharField(db_column="age", default="", max_length=3),
        ),
        migrations.AlterField(
            model_name="patient",
            name="name",
            field=models.CharField(db_column="name", default="", max_length=45),
        ),
    ]
