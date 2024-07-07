from django.db import models
from django.utils.translation import gettext_lazy as _
from ..specialties import models as specialties_models


class Time(models.TextChoices):
    FULLTIME = 'كلي'
    PART_TIME = 'جزئي'


class Degree(models.TextChoices):
    PHD = 'مدرس'
    MASTER = 'ماستر'


class Staff(models.Model):

    class Meta:
        verbose_name_plural = 'Staff'
        ordering = [
            'specialty',
            '-is_countable',
            '-degree',
            '-time',
            '-is_local',
            'name',
        ]

    name = models.CharField(
        max_length=255, 
        unique=True, 
        verbose_name=_('Name')
    )
    specialty = models.ForeignKey(
        specialties_models.Specialty,
        on_delete=models.PROTECT,
        related_name='staff',
        verbose_name=_('Specialty'),
        help_text=_('Specialty in one faculty'),
    )
    degree = models.CharField(
        max_length=255, 
        choices=Degree.choices,
        default=Degree.PHD,
        verbose_name=_('Degree'),
        help_text=_('Degree e.g.: PHD or Master')
    )
    time = models.CharField(
        max_length=255, 
        choices=Time.choices,
        default=Time.FULLTIME,
        verbose_name=_('Time'),
        help_text=_('Time e.g.: Fulltime or part time')
    )
    is_local = models.BooleanField(
        default=False,
        verbose_name=_('Is local'),
        help_text=_('Is local or foreign')
    )
    is_countable = models.BooleanField(
        default=True,
        verbose_name=_('Is countable'),
        help_text=_('To be calculated in capacity or local functions')
    )
    notes = models.TextField(
        max_length=1000, 
        null=True, 
        blank=True,
        verbose_name=_('Notes')
    )
    
    def __str__(self) -> str:
        return f'{self.name} - {self.specialty.faculty.name}'
