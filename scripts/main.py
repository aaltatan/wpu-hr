from apps.faculties import models as faculties_models
from apps.staff import models as staff_models
from django.db.models import Model
from rich import print
import math


class Faculty:
    def __init__(
        self, name: str, 
        staff_model: Model,
        faculty_model: Model,
        time_enum_model: staff_models.Time,
        degree_enum_model: staff_models.Degree,
        specialty_enum_model: staff_models.Specialty,
    ) -> None:
            self.name = name
            self.staff_model = staff_model
            self.faculty_model = faculty_model
            self.time_enum_model = time_enum_model
            self.degree_enum_model = degree_enum_model
            self.specialty_enum_model = specialty_enum_model

    def _get_faculty_instance(self) -> Model:
        return self.faculty_model.objects.filter(name=self.name).first()

    def _get_staff_counts(self, is_countable: bool = True, **kwargs) -> int:
        """
        return staff count based on given filters
        """
        return (
            self
            .staff_model
            .objects
            .filter(is_countable=is_countable, **kwargs)
            .values()
            .count()
        )
    
    @property
    def ratio_specialist_support(self) -> int:
        return self._get_faculty_instance().ratio_specialist_support
    
    @property
    def ratio_count(self) -> int:
        return self._get_faculty_instance().ratio_count
    
    @property
    def fulltime_specialist_phd_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.FULLTIME,
            "specialty": self.specialty_enum_model.SPECIALIST,
            "faculty__name": self.name,
        }
        return self._get_staff_counts(**filters)
    
    @property
    def fulltime_phd_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.FULLTIME,
            "faculty__name": self.name,
        }
        return self._get_staff_counts(**filters)
    
    @property
    def part_time_phd_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.PART_TIME,
            "faculty__name": self.name,
        }
        return self._get_staff_counts(**filters)
    
    @property
    def part_time_specialist_phd_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.PART_TIME,
            "specialty": self.specialty_enum_model.SPECIALIST,
            "faculty__name": self.name,
        }
        return self._get_staff_counts(**filters)
    
    @property
    def fulltime_supporter_phd_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.FULLTIME,
            "specialty": self.specialty_enum_model.SUPPORTER,
            "faculty__name": self.name,
        }
        return self._get_staff_counts(**filters)
    
    @property
    def part_time_supporter_phd_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.PART_TIME,
            "specialty": self.specialty_enum_model.SUPPORTER,
            "faculty__name": self.name,
        }
        return self._get_staff_counts(**filters)
    
    @property
    def fulltime_specialist_masters_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.FULLTIME,
            "specialty": self.specialty_enum_model.SPECIALIST,
            "faculty__name": self.name,
        }
        return self._get_staff_counts(**filters)
    
    @property
    def part_time_specialist_masters_count(self) -> int:
        filters: dict[str, str] = {
            "degree": self.degree_enum_model.PHD,
            "time": self.time_enum_model.PART_TIME,
            "specialty": self.specialty_enum_model.SPECIALIST,
            "faculty__name": self.name,
        }
        return self._get_staff_counts(**filters)
    
    @property
    def specialist_count(self) -> int:

        part_time_specialist_phd_count = 0
        part_time_specialist_masters_count = 0

        if self.part_time_specialist_phd_count > self.fulltime_specialist_phd_count:
            part_time_specialist_phd_count = self.fulltime_specialist_phd_count

        if self.part_time_specialist_masters_count > self.fulltime_specialist_masters_count:
            part_time_specialist_masters_count = self.fulltime_specialist_masters_count

        specialist_phd_count = (
            part_time_specialist_phd_count + self.fulltime_specialist_phd_count
        )

        specialist_master_count = (
            part_time_specialist_masters_count + self.fulltime_specialist_masters_count
        )

        return specialist_phd_count + math.ceil(specialist_master_count / 2)

    @property
    def supporter_count_allowed(self) -> int:
        part_time_supporter_phd_count = 0

        if part_time_supporter_phd_count > self.fulltime_supporter_phd_count:
            part_time_supporter_phd_count = self.fulltime_supporter_phd_count

        makloob_ratio_specialist_support = 100 - self.ratio_specialist_support
        return math.ceil(
            (self.specialist_count * self.ratio_specialist_support) / makloob_ratio_specialist_support
        )
    
    @property
    def supporter_count(self) -> int:
        part_time_supporter_phd_count = 0

        if part_time_supporter_phd_count > self.fulltime_supporter_phd_count:
            part_time_supporter_phd_count = self.fulltime_supporter_phd_count

        supporter_phd_count = self.fulltime_supporter_phd_count + part_time_supporter_phd_count

        return min(supporter_phd_count, self.supporter_count_allowed)

    def get_capacity_respecting_specialty(self) -> int:
        """
        calculate the capacity of specific faculty
        """
        staff_count = self.supporter_count + self.specialist_count
        capacity = staff_count * self.ratio_count
        return capacity
    
    def get_capacity_ignoring_specialty(self):
        part_time_phd_count = 0
        part_time_masters_count = 0

        if self.part_time_phd_count > self.fulltime_phd_count:
            part_time_phd_count = self.fulltime_phd_count

        if self.part_time_specialist_masters_count > self.fulltime_specialist_masters_count:
            part_time_masters_count = self.fulltime_specialist_masters_count

        phd_count = (
            part_time_phd_count + self.fulltime_phd_count
        )

        master_count = (
            part_time_masters_count + self.fulltime_specialist_masters_count
        )

        staff_count = phd_count + math.ceil(master_count / 2)
        capacity = staff_count * self.ratio_count

        return capacity
    
    def __part_over_warning(self, part: int, full: int, key: str = '') -> dict | None:
        if part > full:
            return {
                'message': f'زيادة في أعضاء الهيئة التدريسية {key} المفرغين جزئياً'.strip(),
                'count': part - full
            }
        return
    
    def __supporter_over_warning(self, part: int, full: int, key: str = '') -> dict | None:
        if part > full:
            return {
                'message': f'زيادة في أعضاء الهيئة التدريسية {key} المفرغين جزئياً'.strip(),
                'count': part - full
            }
        return
    
    def get_warnings(self, ignoring_specialty: bool = True) -> list[dict | None]:
        warnings: list = []

        if ignoring_specialty:
            w = self.__part_over_warning(self.part_time_phd_count,
                                     self.fulltime_phd_count)
            warnings.append(w)
        else:
            w = self.__part_over_warning(self.part_time_specialist_phd_count,
                                     self.fulltime_specialist_phd_count,
                                     'التخصصيين')
            warnings.append(w)
            
            w = self.__part_over_warning(self.part_time_supporter_phd_count,
                                     self.fulltime_supporter_phd_count,
                                     'الداعمين')
            warnings.append(w)

        return [w for w in warnings if w]



def run() -> None:

    faculty = Faculty(
        name='طب الأسنان', 
        staff_model=staff_models.Staff,
        faculty_model=faculties_models.Faculty,
        degree_enum_model=staff_models.Degree,
        specialty_enum_model=staff_models.Specialty,
        time_enum_model=staff_models.Time
    )
    
    capacity_ignore = faculty.get_capacity_ignoring_specialty()
    capacity_respect = faculty.get_capacity_respecting_specialty()
    print(capacity_ignore)
    print(capacity_respect)
