# Generated by Django 5.0.6 on 2024-06-05 10:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_faculty_ratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='ratio_count',
            field=models.PositiveBigIntegerField(default=35, validators=[django.core.validators.MinValueValidator(0, 'count must be more than 0')]),
        ),
        migrations.AddField(
            model_name='faculty',
            name='ratio_staff_count',
            field=models.PositiveBigIntegerField(default=20, validators=[django.core.validators.MinValueValidator(0, 'count must be more than 0')]),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='ratio',
            field=models.PositiveBigIntegerField(default=50, validators=[django.core.validators.MinValueValidator(0, 'count must be more than 0'), django.core.validators.MaxValueValidator(100, 'count must be less than 100')]),
        ),
    ]
