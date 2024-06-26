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

    name = models.CharField(max_length=255, unique=True, verbose_name='الإسم')
    faculty = models.ForeignKey(
        faculties_models.Faculty,
        on_delete=models.PROTECT,
        related_name='staff',
        verbose_name='الكلية',
        help_text='الكلية'
    )
    specialty = models.CharField(
        max_length=255, 
        choices=Specialty.choices,
        default=Specialty.SPECIALIST,
        verbose_name='التخصص',
        help_text='التخصص اختصاصي، داعم'
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
    is_staff = models.BooleanField(
        default=True,
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
        return f'{self.name} | {self.faculty.name}'
