# Generated by Django 5.0.6 on 2024-07-10 08:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("faculties", "0011_alter_faculty_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="faculty",
            name="count_of_graduates",
            field=models.PositiveBigIntegerField(
                default=0,
                help_text="graduates count",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="graduates count",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="count_of_students",
            field=models.PositiveBigIntegerField(
                default=0,
                help_text="count of students exclude graduates and scholarship",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="students count",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="local_staff_percentage",
            field=models.PositiveBigIntegerField(
                default=50,
                help_text="allowed local staff percentage",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    ),
                    django.core.validators.MaxValueValidator(
                        100, "count must be less than 100"
                    ),
                ],
                verbose_name="local staff percentage",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="name",
            field=models.CharField(max_length=255, unique=True, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="student_to_local_teacher_count",
            field=models.PositiveBigIntegerField(
                default=20,
                help_text="students to local teachers count",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="students to local teachers count",
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="student_to_teacher_count",
            field=models.PositiveBigIntegerField(
                default=35,
                help_text="students to teachers count",
                validators=[
                    django.core.validators.MinValueValidator(
                        0, "count must be more than 0"
                    )
                ],
                verbose_name="students to teachers count",
            ),
        ),
    ]
