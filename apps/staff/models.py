from django.db import models
from ..faculties import models as faculties_models


class Time(models.TextChoices):
    FULLTIME = "كلي"
    PART_TIME = "جزئي"


class Degree(models.TextChoices):
    PHD = "مدرس"
    MASTER = "ماستر"


class Specialty(models.TextChoices):
    SPECIALIST = "اختصاصي"
    SUPPORTER = "داعم"


class Staff(models.Model):

    class Meta:
        verbose_name_plural = 'Staff'

    name = models.CharField(max_length=255, unique=True)
    faculty = models.ForeignKey(
        faculties_models.Faculty,
        on_delete=models.PROTECT,
        related_name='staff'
    )
    specialty = models.CharField(
        max_length=255, 
        choices=Specialty.choices,
        default=Specialty.SPECIALIST
    )
    degree = models.CharField(
        max_length=255, 
        choices=Degree.choices,
        default=Degree.PHD
    )
    time = models.CharField(
        max_length=255, 
        choices=Time.choices,
        default=Time.FULLTIME
    )
    is_staff = models.BooleanField(default=True)
    is_countable = models.BooleanField(default=True)
    notes = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name} | {self.faculty.name}'
