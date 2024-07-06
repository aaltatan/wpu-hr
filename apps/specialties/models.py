from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from ..faculties import models as faculties_models


class Specialty(models.Model):
    
    class Meta:
        ordering = ['faculty__name']
        verbose_name_plural = 'Specialties'
    
    faculty = models.ForeignKey(
        faculties_models.Faculty, 
        on_delete=models.PROTECT, 
        related_name='specialties'
    )
    name = models.CharField(
        max_length=255, 
        help_text='اسم التخصص', 
        verbose_name='اسم التخصص',
    )
    percentage = models.PositiveIntegerField(
        validators=faculties_models.rate_validator,
        default=65,
        help_text='نسبة التخصص', 
        verbose_name='نسبة التخصص'
    )
    is_specialist = models.BooleanField(
        help_text='اختصاصي',
        verbose_name='اختصاصي',
        default=False
    )
    
    def save(self, *args, **kwargs) -> None:
        
        if self.is_specialist:
            specialties = (
                Specialty
                .objects
                .filter(faculty__name=self.faculty.name)
            )
            for s in specialties:
                s.is_specialist = False
                s.save()
        
        return super().save(*args, **kwargs)
    
    def clean(self) -> None:
        
        primary_key = getattr(self, 'pk')
        stmt = Q(faculty__name=self.faculty.name)
        
        if primary_key:
            stmt &= ~Q(pk=primary_key)
        
        total_percentage = (
            Specialty
            .objects
            .filter(stmt)
            .aggregate(total=Sum('percentage'))
        )
        total = total_percentage['total'] or 0
        allowed_percentage = 100 - total
        total += self.percentage
        
        if total > 100:
            raise ValidationError(f'you CAN\'T add more than 100% per faculty 😢, you could add up to {allowed_percentage}% only.')
    
    def __str__(self) -> str:
        return f'{self.faculty.name} - {self.name}'