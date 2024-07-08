from ..faculties import models as faculties_models
from ..specialties import models as specialties_models
from ..staff import models as staff_models
from django.db.models import QuerySet
import pandas as pd
import math
from rich import print


class FacultyController:
    def __init__(
        self,
        faculty_model: faculties_models.Faculty,
        time_enum_model: staff_models.Time,
        degree_enum_model: staff_models.Degree,
    ) -> None:
        self.faculty_model: faculties_models.Faculty = faculty_model
        self.time_enum_model: staff_models.Time = time_enum_model
        self.degree_enum_model:staff_models.Degree = degree_enum_model

    def __get_staff_count(self, filters: dict) -> int:
        
        specialties_filters: dict = filters.get('specialties_filters', {})
        staff_filters: dict = filters.get('staff_filters', {})
        staff_filters['is_countable'] = staff_filters.get('staff_filters', True)
        
        specialties = (
            self
            .faculty_model
            .specialties
            .filter(**specialties_filters)
        )
        with open('file.txt', 'a', encoding='utf-8') as file:
            file.write('1\n')
        return sum(
            specialty.staff.filter(**staff_filters).count()
            for specialty in specialties
        )
        
    @property
    def specialist_fulltime_phd_count(self) -> int:
        filters: dict[str, dict] = {
            'specialties_filters': {'is_specialist': True},
            'staff_filters': {
                'degree': self.degree_enum_model.PHD,
                'time': self.time_enum_model.FULLTIME,
            }
        }
        return self.__get_staff_count(filters)
        
    @property
    def supporters_fulltime_phd_count(self) -> int:
        filters: dict[str, dict] = {
            'specialties_filters': {'is_specialist': False},
            'staff_filters': {
                'degree': self.degree_enum_model.PHD,
                'time': self.time_enum_model.FULLTIME,
            }
        }
        return self.__get_staff_count(filters)
        
    @property
    def specialist_parttime_phd_count(self) -> int:
        filters: dict[str, dict] = {
            'specialties_filters': {'is_specialist': True},
            'staff_filters': {
                'degree': self.degree_enum_model.PHD,
                'time': self.time_enum_model.PART_TIME,
            }
        }
        return self.__get_staff_count(filters)
        
    @property
    def supporters_parttime_phd_count(self) -> int:
        filters: dict[str, dict] = {
            'specialties_filters': {'is_specialist': False},
            'staff_filters': {
                'degree': self.degree_enum_model.PHD,
                'time': self.time_enum_model.PART_TIME,
            }
        }
        return self.__get_staff_count(filters)
        
    @property
    def masters_count(self) -> int:
        filters: dict[str, dict] = {
            'specialties_filters': {'is_specialist': True},
            'staff_filters': {
                'degree': self.degree_enum_model.MASTER,
                'time': self.time_enum_model.FULLTIME,
            }
        }
        return self.__get_staff_count(filters)
    
    @property
    def students_count(self) -> int:
        return (
            self.faculty_model.count_of_students -
            self.faculty_model.count_of_scholarship_students -
            self.faculty_model.count_of_graduates
        )
        
    def __get_allowed_parttime_count(
        self, 
        fulltime_count: int,
        parttime_count: int,
    ) -> int:
        if fulltime_count < parttime_count:
            return fulltime_count
        return parttime_count
    
    def __get_allowed_masters_count(self, count: int) -> float:
        return count / 2
    
    def __get_allowed_supporters_count(
        self,
        specialist_count: float,
        specialist_percentage: float,
        percentage: int
    ) -> int:
        return math.floor(
            specialist_count * percentage / specialist_percentage
        )
    
    def __get_supporters_counts(self) -> dict:
        
        result: dict = {
            'specialist_percentage': 0,
            'counts': [],
        }
        
        supporter_specialties: QuerySet[specialties_models.Specialty] = (
            self
            .faculty_model
            .specialties
            .all()
        )
        
        for specialty in supporter_specialties:
            
            if not specialty.is_specialist:
                staff_filters: dict[str, dict] = {
                    'degree': self.degree_enum_model.PHD,
                    'time': self.time_enum_model.FULLTIME,
                    'specialty__name': specialty.name,
                    'is_countable': True,
                }
                
                fulltime_count = specialty.staff.filter(**staff_filters).count()
                
                staff_filters['time'] = self.time_enum_model.PART_TIME
                parttime_count = specialty.staff.filter(**staff_filters).count()
                
                result['counts'].append({
                    'percentage': specialty.percentage, 
                    'fulltime_count': fulltime_count,
                    'parttime_count': parttime_count,
                })
            else:
                result['specialist_percentage'] = specialty.percentage
                
        return result
    
    def get_capacity_without_supporters_percentage(
            self,
            respect_supporters_partials: bool = True
        ) -> float:
        
        masters_count = self.__get_allowed_masters_count(self.masters_count)
        parttime_phd_count = 0
        fulltime_phd_count = (
            self.specialist_fulltime_phd_count + 
            self.supporters_fulltime_phd_count
        )
        
        if respect_supporters_partials:
            specialist_parttime_phd_count = self.__get_allowed_parttime_count(
                self.specialist_fulltime_phd_count,
                self.specialist_parttime_phd_count,
            )
            supporters_parttime_phd_count = self.__get_allowed_parttime_count(
                self.supporters_fulltime_phd_count,
                self.supporters_parttime_phd_count,
            )
            parttime_phd_count = (
                specialist_parttime_phd_count +
                supporters_parttime_phd_count
            )
        else:
            parttime_phd_count = self.__get_allowed_parttime_count(
                fulltime_phd_count,
                self.specialist_parttime_phd_count +
                self.supporters_parttime_phd_count
            )
        
        return (
            fulltime_phd_count +
            parttime_phd_count +
            masters_count
        ) * self.faculty_model.student_to_teacher_count
    
    def get_capacity_with_supporters_percentage(self) -> float:
        
        supporters_count = 0
        
        masters_count = self.__get_allowed_masters_count(self.masters_count)
        specialist_fulltime_phd_count = self.specialist_fulltime_phd_count
        specialist_parttime_phd_count = self.__get_allowed_parttime_count(
            self.specialist_fulltime_phd_count,
            self.specialist_parttime_phd_count
        )
        
        specialist_count = (
            specialist_fulltime_phd_count +
            specialist_parttime_phd_count +
            masters_count
        )
        
        supporter_counts = self.__get_supporters_counts()
        specialist_percentage, counts = supporter_counts.values()
        
        for count in counts:
            allowed_supporters_count = self.__get_allowed_supporters_count(
                specialist_count,
                specialist_percentage,
                count['percentage'],
            )
            supporters_fulltime_count = count['fulltime_count']
            supporters_parttime_count = 0
            
            if supporters_fulltime_count >= allowed_supporters_count:
                supporters_fulltime_count = allowed_supporters_count
            else:
                supporters_parttime_count = allowed_supporters_count - supporters_fulltime_count
        
            supporters_parttime_count = self.__get_allowed_parttime_count(
                supporters_fulltime_count,
                supporters_parttime_count
            )
            
            specialty_count = supporters_fulltime_count + supporters_parttime_count
            
            supporters_count += specialty_count
            
        total_count = specialist_count + supporters_count
        
        return total_count * self.faculty_model.student_to_teacher_count
    
    def get_required_local_teachers_count(
        self,
    ) -> float:
        return (
            self.students_count /
            2 / # chapters
            5 / # count of years by ministry
            self.faculty_model.student_to_local_teacher_count
        ) * 5 # current year by ministry
      
    def get_local_staff_count(self, include_masters: bool = False) -> float | int:
        phd_filters: dict[str, dict] = {
            'staff_filters': {
                'degree': self.degree_enum_model.PHD,
                'is_local': True,
            }
        }
        master_filters: dict[str, dict] = {
            'staff_filters': {
                'degree': self.degree_enum_model.MASTER,
                'is_local': True,
            }
        }
        phd_count = self.__get_staff_count(phd_filters)
        master_count = self.__get_staff_count(master_filters)
        master_count = self.__get_allowed_masters_count(master_count)
        
        total = phd_count + master_count
            
        return total if include_masters else phd_count