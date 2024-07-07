# Generated by Django 5.0.6 on 2024-07-06 10:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("faculties", "0010_remove_faculty_supporters_percentage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="faculty",
            options={"ordering": ["name"], "verbose_name_plural": "Faculties"},
        ),
        migrations.AlterField(
            model_name="faculty",
            name="count_of_graduates",
            field=models.PositiveBigIntegerField(
                default=0,
                help_text="Graduates count",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="Graduates count",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="count_of_scholarship_students",
            field=models.PositiveBigIntegerField(
                default=0,
                help_text="scholarship students count",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="scholarship students count",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="count_of_students",
            field=models.PositiveBigIntegerField(
                default=0,
                help_text="Count of students exclude graduates and scholarship",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="Students count",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="local_staff_percentage",
            field=models.PositiveBigIntegerField(
                default=50,
                help_text="Allowed local staff percentage",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    ),
                    django.core.validators.MaxValueValidator(
                        100, "count must be less than 100"
                    ),
                ],
                verbose_name="Local staff percentage",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="name",
            field=models.CharField(max_length=255, unique=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="student_to_local_teacher_count",
            field=models.PositiveBigIntegerField(
                default=20,
                help_text="Students to local teachers count",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="Students to local teachers count",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="student_to_teacher_count",
            field=models.PositiveBigIntegerField(
                default=35,
                help_text="Students to teachers count",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="Students to teachers count",
            ),
        ),
    ]