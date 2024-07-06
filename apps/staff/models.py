from django.db import models
from ..specialties import models as specialties_models


class Time(models.TextChoices):
    FULLTIME = "كلي"
    PART_TIME = "جزئي"


class Degree(models.TextChoices):
    PHD = "مدرس"
    MASTER = "ماستر"


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

    name = models.CharField(max_length=255, unique=True, verbose_name='الإسم')
    specialty = models.ForeignKey(
        specialties_models.Specialty,
        on_delete=models.PROTECT,
        related_name='staff',
        verbose_name='الاختصاص',
        help_text='الاختصاص ضمن الكلية الواحدة'
    )
    degree = models.CharField(
        max_length=255, 
        choices=Degree.choices,
        default=Degree.PHD,
        verbose_name='الدرجة العلمية',
        help_text='الدرجة العلمية دكتور، مدرس'
    )
    time = models.CharField(
        max_length=255, 
        choices=Time.choices,
        default=Time.FULLTIME,
        verbose_name='التفرغ',
        help_text='التفرغ جزئي ، كلي'
    )
    is_local = models.BooleanField(
        default=False,
        verbose_name='ملاك',
        help_text='ضمن ملاك الجامعة الوطنية'
    )
    is_countable = models.BooleanField(
        default=True,
        verbose_name='يحتسب',
        help_text='لن يتم احتسابه ضمن معادلات حساب الطاقة أو الملاك و غيرها'
    )
    notes = models.TextField(
        max_length=1000, 
        null=True, 
        blank=True,
        verbose_name='ملاحظات'
    )
    
    def __str__(self) -> str:
        return f'{self.name} - {self.specialty.faculty.name}'
