from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from ..faculties import models as faculties_models


class FacultySupporter(models.Model):
    faculty = models.ForeignKey(
        faculties_models.Faculty, 
        on_delete=models.PROTECT, 
        related_name='supporters'
    )
    name = models.CharField(
        max_length=255, 
        help_text='اسم التخصص الداعم', 
        verbose_name='اسم التخصص الداعم',
    )
    percentage = models.PositiveIntegerField(
        validators=faculties_models.rate_validator,
        default=35,
        help_text='نسبة التخصص الداعم', 
        verbose_name='نسبة التخصص الداعم'
    )
    
    def __str__(self) -> str:
        return f'{self.faculty.name} [{self.name} - {self.percentage}%]'
    
    def clean(self) -> None:
        
        primary_key = getattr(self, 'pk')
        stmt = Q(faculty__name=self.faculty.name)
        
        if primary_key:
            stmt &= ~Q(pk=primary_key)
        
        total_percentage = (
            FacultySupporter
            .objects
            .filter(stmt)
            .aggregate(total=Sum('percentage'))
        )
        total = total_percentage['total'] or 0
        allowed_percentage = 100 - total
        total += self.percentage
        
        if total > 100:
            raise ValidationError(f'you CAN\'T add more than 100% per faculty 😢, you could add up to {allowed_percentage}% only.')
        