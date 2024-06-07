from typing import Any
from apps.base import models as base_models
from apps.staff import models as staff_models
from icecream import ic


def get_staff_counts(is_countable: bool = True, **kwargs) -> int:
    '''
    return staff count based on given filters
    '''
    return (
        staff_models
        .Staff
        .objects
        .filter(
            is_countable=is_countable,
            **kwargs
        )
        .values()
        .count()
    )


def get_capacity_inputs(faculty_name: str) -> dict[str, int | str]:
    '''
    return the whole capacity inputs to calculate the capacity
    '''
    faculty = base_models.Faculty.objects.filter(name=faculty_name).first()

    filters: dict[str, Any] = {
        'degree': staff_models.Degree.PHD,
        'time': staff_models.Time.FULLTIME,
        'specialty': staff_models.Specialty.SPECIALIST,
        'faculty__name': faculty_name,
    }

    fulltime_specialist_phd_count = get_staff_counts(**filters)

    filters['time'] = staff_models.Time.PART_TIME
    part_time_specialist_phd_count = get_staff_counts(**filters)

    filters['time'] = staff_models.Time.FULLTIME
    filters['specialty'] = staff_models.Specialty.SUPPORTER
    fulltime_supporter_phd_count = get_staff_counts(**filters)

    filters['time'] = staff_models.Time.PART_TIME
    part_time_supporter_phd_count = get_staff_counts(**filters)

    filters['degree'] = staff_models.Degree.MASTER
    filters['time'] = staff_models.Time.FULLTIME
    filters['specialty'] = staff_models.Specialty.SPECIALIST
    fulltime_specialist_masters_count = get_staff_counts(**filters)

    filters['time'] = staff_models.Time.PART_TIME
    part_time_specialist_masters_count = get_staff_counts(**filters)

    return {
        'faculty': faculty_name,
        'ratio_specialist_support': faculty.ratio_specialist_support,
        'ratio_count': faculty.ratio_count,
        'fulltime_specialist_phd_count': fulltime_specialist_phd_count,
        'part_time_specialist_phd_count': part_time_specialist_phd_count,
        'fulltime_supporter_phd_count': fulltime_supporter_phd_count,
        'part_time_supporter_phd_count': part_time_supporter_phd_count,
        'fulltime_specialist_masters_count': fulltime_specialist_masters_count,
        'part_time_specialist_masters_count': part_time_specialist_masters_count,
    }


def generate_warning_between_full_part(
    fulltime_count: int,
    part_time_count: int,
    faculty_name: str,
    specialty: str = 'الاختصاصيين',
    degree: str = 'مدرسين',
) -> str:
    difference = abs(fulltime_count - part_time_count)
    warning = f'مدرسين الجزئي الاختصاصيين أكثر من مدرسي الكلي بفارق' + \
              str(difference) + \
              " | " + \
              faculty_name
    return warning


def calculate_capacity(
    faculty_name: str,
    ratio_specialist_support: int,
    ratio_count: int,
    fulltime_specialist_phd_count: int,
    part_time_specialist_phd_count: int,
    fulltime_supporter_phd_count: int,
    part_time_supporter_phd_count: int,
    fulltime_specialist_masters_count: int,
    part_time_specialist_masters_count: int,
) -> dict[str, Any]:
    '''
    calculate the capacity of specific faculty
    '''

    warnings_list: list[str] = []

    if fulltime_specialist_phd_count < part_time_specialist_phd_count:
        difference = \
          abs(fulltime_specialist_phd_count - part_time_specialist_phd_count)
        warning = 'مدرسين الجزئي الاختصاصيين أكثر من مدرسي الكلي بفارق' + \
                  str(difference) + \
                  " | " + \
                  faculty_name
        warnings_list.append(warning)

    if fulltime_supporter_phd_count < part_time_supporter_phd_count:
        difference = \
          abs(fulltime_supporter_phd_count - part_time_supporter_phd_count)
        warning = 'مدرسين الجزئي الداعمين أكثر من مدرسي الكلي بفارق' + \
                  str(difference) + \
                  " | " + \
                  faculty_name
        warnings_list.append(warning)


    


def run() -> None:
    faculties: list[str] = [
        'طب الأسنان',
        'dasd',
    ]

    inputs = get_capacity_inputs(faculties[0])

    ic(inputs)
