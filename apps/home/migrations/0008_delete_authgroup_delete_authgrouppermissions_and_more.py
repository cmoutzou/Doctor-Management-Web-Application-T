# Generated by Django 4.1 on 2022-09-08 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_authgroup_authgrouppermissions_authpermission_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="AuthGroup",),
        migrations.DeleteModel(name="AuthGroupPermissions",),
        migrations.DeleteModel(name="AuthPermission",),
        migrations.DeleteModel(name="AuthUser",),
        migrations.DeleteModel(name="AuthUserGroups",),
        migrations.DeleteModel(name="AuthUserUserPermissions",),
        migrations.DeleteModel(name="DjangoAdminLog",),
        migrations.DeleteModel(name="DjangoContentType",),
        migrations.DeleteModel(name="DjangoMigrations",),
        migrations.DeleteModel(name="DjangoSession",),
    ]