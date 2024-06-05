from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Faculty(models.Model):
    
    class Meta:
        verbose_name_plural = 'Faculties'

    name = models.CharField(max_length=255, unique=True)
    count_of_scholarship_students = models.PositiveBigIntegerField(
        default=0,
        validators=[MinValueValidator(0, 'count must be more than 0')]
    )
    count_of_graduates = models.PositiveBigIntegerField(
        default=0,
        validators=[MinValueValidator(0, 'count must be more than 0')]
    )
    count_of_students = models.PositiveBigIntegerField(
        default=0,
        validators=[MinValueValidator(0, 'count must be more than 0')]
    )
    count_of_new_students = models.PositiveBigIntegerField(
        default=0,
        validators=[MinValueValidator(0, 'count must be more than 0')]
    )
    ratio = models.PositiveBigIntegerField(
        default=50,
        validators=[
            MinValueValidator(0, 'count must be more than 0'),
            MaxValueValidator(100, 'count must be less than 100'),
        ]
    )
    ratio_count = models.PositiveBigIntegerField(
        default=35,
        validators=[MinValueValidator(0, 'count must be more than 0')]
    )
    ratio_staff_count = models.PositiveBigIntegerField(
        default=20,
        validators=[MinValueValidator(0, 'count must be more than 0')]
    )

    def __str__(self) -> str:
        return self.name