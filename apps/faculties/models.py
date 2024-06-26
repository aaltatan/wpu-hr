from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

count_validator = [MinValueValidator(0, 'count must be more than 0')]
rate_validator = [
    MinValueValidator(0, 'count must be more than 0'),
    MaxValueValidator(100, 'count must be less than 100'),
]

class Faculty(models.Model):
    
    class Meta:
        verbose_name_plural = 'Faculties'

    name = models.CharField(max_length=255, unique=True, verbose_name='الإسم')
    count_of_scholarship_students = models.PositiveBigIntegerField(
        default=0,
        validators=count_validator,
        help_text="عدد طلاب المنح",
        verbose_name='عدد طلاب المنح'
    )
    count_of_graduates = models.PositiveBigIntegerField(
        default=0,
        validators=count_validator,
        help_text="عدد الخريجين",
        verbose_name="عدد الخريجين",
    )
    count_of_students = models.PositiveBigIntegerField(
        default=0,
        validators=count_validator,
        help_text="عدد الطلاب متضمن الخريجين والمنح",
        verbose_name="عدد الطلاب",
    )
    supporters_percentage = models.PositiveBigIntegerField(
        default=30,
        validators=rate_validator,
        help_text='نسبة الداعم الى الاختصاصي',
        verbose_name='نسبة الداعم',
    )
    local_staff_percentage = models.PositiveBigIntegerField(
        default=50,
        validators=rate_validator,
        help_text='نسبة الملاك الذي يجب تحقيقها',
        verbose_name='نسبة الملاك الوزارة',
    )
    student_to_teacher_count = models.PositiveBigIntegerField(
        default=35,
        validators=count_validator,
        help_text='عدد الطلاب المسموح به لكل مدرس',
        verbose_name='عدد الطلاب لكل مدرس',
    )
    student_to_local_teacher_count = models.PositiveBigIntegerField(
        default=20,
        validators=count_validator,
        help_text='عدد الطلاب حسب الاعتمادية (الملاك)',
        verbose_name='عدد الطلاب (الاعتمادية)',
    )

    def __str__(self) -> str:
        return self.name