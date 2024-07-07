from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


count_validator = [ MinValueValidator(0, _('count must be more than 0')) ]
rate_validator = [
    MinValueValidator(0, _('count must be more than 0')),
    MaxValueValidator(100, _('count must be less than 100')),
]

class Faculty(models.Model):
    
    class Meta:
        verbose_name_plural = 'Faculties'
        ordering = ['name']

    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    count_of_scholarship_students = models.PositiveBigIntegerField(
        default=0,
        validators=count_validator,
        help_text=_('scholarship students count'),
        verbose_name=_('scholarship students count')
    )
    count_of_graduates = models.PositiveBigIntegerField(
        default=0,
        validators=count_validator,
        help_text=_('Graduates count'),
        verbose_name=_('Graduates count'),
    )
    count_of_students = models.PositiveBigIntegerField(
        default=0,
        validators=count_validator,
        help_text=_('Count of students exclude graduates and scholarship'),
        verbose_name=_('Students count'),
    )
    local_staff_percentage = models.PositiveBigIntegerField(
        default=50,
        validators=rate_validator,
        help_text=_('Allowed local staff percentage'),
        verbose_name=_('Local staff percentage'),
    )
    student_to_teacher_count = models.PositiveBigIntegerField(
        default=35,
        validators=count_validator,
        help_text=_('Students to teachers count'),
        verbose_name=_('Students to teachers count'),
    )
    student_to_local_teacher_count = models.PositiveBigIntegerField(
        default=20,
        validators=count_validator,
        help_text=_('Students to local teachers count'),
        verbose_name=_('Students to local teachers count'),
    )

    def __str__(self) -> str:
        return self.name