from apps.faculties import models as faculties_models
from apps.staff import models as staff_models
from django.db.models import Model
from rich import print
import math


class FacultyController:
    def __init__(
        self,
        faculty_model: faculties_models.Faculty,
        time_enum_model: staff_models.Time,
        degree_enum_model: staff_models.Degree,
        specialty_enum_model: staff_models.Specialty,
    ) -> None:
        self.faculty_model = faculty_model
        self.time_enum_model = time_enum_model
        self.degree_enum_model = degree_enum_model
        self.specialty_enum_model = specialty_enum_model

    def _get_staff_counts(self, **kwargs) -> int:
        """
        return staff count based on given filters
        """
        kwargs['is_countable'] = kwargs.get('is_countable', True)
        return self.faculty_model.staff.filter(**kwargs).count()

    @property
    def supporters_percentage(self) -> int:
        return self.faculty_model.supporters_percentage

    @property
    def student_to_teacher_count(self) -> int:
        return self.faculty_model.student_to_teacher_count

    @property
    def fulltime_phd_specialist_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.FULLTIME,
            "specialty": self.specialty_enum_model.SPECIALIST,
        }
        return self._get_staff_counts(**filters)

    @property
    def fulltime_phd_supporter_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.FULLTIME,
            "specialty": self.specialty_enum_model.SUPPORTER,
        }
        return self._get_staff_counts(**filters)

    @property
    def fulltime_phd_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.FULLTIME,
        }
        return self._get_staff_counts(**filters)

    @property
    def part_time_phd_specialist_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.PART_TIME,
            "specialty": self.specialty_enum_model.SPECIALIST,
        }
        return self._get_staff_counts(**filters)

    @property
    def part_time_phd_supporter_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.PART_TIME,
            "specialty": self.specialty_enum_model.SUPPORTER,
        }
        return self._get_staff_counts(**filters)

    @property
    def part_time_phd_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.PART_TIME,
        }
        return self._get_staff_counts(**filters)

    @property
    def fulltime_master_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.MASTER,
            "time": self.time_enum_model.FULLTIME,
        }
        return self._get_staff_counts(**filters)

    def _get_allowed_part_time_count(self) -> int:

        part_time_phd_count = self.part_time_phd_count

        if self.fulltime_phd_count < part_time_phd_count:
            part_time_phd_count = self.fulltime_phd_count

        return part_time_phd_count

    def _get_allowed_part_time_specialist_count(self) -> int:

        part_time_phd_specialist_count = self.part_time_phd_specialist_count

        if self.fulltime_phd_specialist_count < part_time_phd_specialist_count:
            part_time_phd_specialist_count = self.fulltime_phd_specialist_count

        return part_time_phd_specialist_count
    
    def _get_allowed_master_count(self, master_count: int) -> int:
        return int(math.ceil(master_count / 2)) ########
    
    def _get_allowed_supporters_count(self, specialist_staff_count: int) -> int:
        allowed_supporter_count = specialist_staff_count * self.supporters_percentage
        allowed_supporter_count /= 100 - self.supporters_percentage
        return math.ceil(allowed_supporter_count) ########

    def get_capacity(self, respect_supporter_ratio: bool = False) -> int:
        
        fulltime_master_count = self._get_allowed_master_count(self.fulltime_master_count)
        
        if not respect_supporter_ratio:
            fulltime_phd_count = self.fulltime_phd_count
            part_time_phd_count = self._get_allowed_part_time_count()
            staff_count = (
                fulltime_phd_count + part_time_phd_count + fulltime_master_count
            )
            return staff_count * self.student_to_teacher_count

        fulltime_phd_specialist_count = self.fulltime_phd_specialist_count
        part_time_phd_specialist_count = self._get_allowed_part_time_specialist_count()
        specialist_staff_count = (
            fulltime_phd_specialist_count
            + part_time_phd_specialist_count
            + fulltime_master_count
        )

        allowed_supporter_count = self._get_allowed_supporters_count(specialist_staff_count)
        fulltime_phd_supporter_count = self.fulltime_phd_supporter_count
        part_time_phd_supporter_count = 0
        
        ########
        if fulltime_phd_supporter_count >= allowed_supporter_count:
            fulltime_phd_supporter_count = allowed_supporter_count
        else:
            part_time_phd_supporter_count = allowed_supporter_count - fulltime_phd_supporter_count
            
        if fulltime_phd_supporter_count <= part_time_phd_supporter_count:
            part_time_phd_supporter_count = fulltime_phd_supporter_count
            
        supporter_staff_count = (
            fulltime_phd_supporter_count + part_time_phd_supporter_count
        )
        #######
        
        staff_count = supporter_staff_count + specialist_staff_count
        
        return staff_count * self.student_to_teacher_count


def run() -> None:

    faculties = faculties_models.Faculty.objects.all()
    
    for faculty in faculties:
    
        print(faculty)
        
        controller = FacultyController(
            faculty_model=faculty,
            degree_enum_model=staff_models.Degree,
            specialty_enum_model=staff_models.Specialty,
            time_enum_model=staff_models.Time,
        )

        capacity_with_respect_supporter = controller.get_capacity(respect_supporter_ratio=True)
        capacity_with_not_respect_supporter = controller.get_capacity()
        
        print(
            f'{capacity_with_respect_supporter=}',
            f'{capacity_with_not_respect_supporter=}',
            sep='\n'
        )
    
    
