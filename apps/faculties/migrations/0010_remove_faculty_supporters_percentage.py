# Generated by Django 5.0.6 on 2024-07-04 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("faculties", "0009_delete_facultysupporter"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="faculty",
            name="supporters_percentage",
        ),
    ]
