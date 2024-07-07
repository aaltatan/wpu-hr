from django.db import models
from django.utils.translation import gettext_lazy as _
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
        help_text=_('The name of specialty'), 
        verbose_name=_('Name'),
    )
    percentage = models.PositiveIntegerField(
        validators=faculties_models.rate_validator,
        default=65,
        help_text=_('Percentage of the specialty'), 
        verbose_name=_('Percentage')
    )
    is_specialist = models.BooleanField(
        help_text=_('Is specialist'),
        verbose_name=_('Is specialist'),
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
            raise ValidationError(
                _('you CAN\'T add more than 100% per faculty, you could add up to {}% only.').format(allowed_percentage)
            )
    
    def __str__(self) -> str:
        return f'{self.faculty.name} - {self.name}'