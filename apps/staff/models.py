from django.db import models
from django.utils.translation import gettext_lazy as _
from ..specialties import models as specialties_models


class Time(models.TextChoices):
    FULLTIME = 'كلي', _('fulltime')
    PART_TIME = 'جزئي', _('parttime')


class Degree(models.TextChoices):
    PHD = 'مدرس', _('phd')
    MASTER = 'ماستر', _('master')


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
        verbose_name=_('name')
    )
    specialty = models.ForeignKey(
        specialties_models.Specialty,
        on_delete=models.PROTECT,
        related_name='staff',
        verbose_name=_('specialty'),
        help_text=_('specialty in one faculty'),
    )
    degree = models.CharField(
        max_length=255, 
        choices=Degree.choices,
        default=Degree.PHD,
        verbose_name=_('degree'),
        help_text=_('degree e.g.: PHD or Master')
    )
    time = models.CharField(
        max_length=255, 
        choices=Time.choices,
        default=Time.FULLTIME,
        verbose_name=_('time'),
        help_text=_('time e.g.: Fulltime or part time')
    )
    is_local = models.BooleanField(
        default=False,
        verbose_name=_('is local'),
        help_text=_('is local or foreign')
    )
    is_countable = models.BooleanField(
        default=True,
        verbose_name=_('is countable'),
        help_text=_('to be calculated in capacity or local functions')
    )
    notes = models.TextField(
        max_length=1000, 
        null=True, 
        blank=True,
        verbose_name=_('notes')
    )
    
    def __str__(self) -> str:
        return f'{self.name} - {self.specialty.faculty.name}'
