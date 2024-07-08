from apps.faculties import models as faculties_models
from apps.staff import models as staff_models
from rich import print
from apps.base.utils import FacultyController


def run() -> None:

    faculties = faculties_models.Faculty.objects.all()
    for fac in faculties:

        controller = FacultyController(fac, staff_models.Time, staff_models.Degree)

        new_capacity_with_respect_supporters = (
            controller.get_capacity_without_supporters_percentage(
                respect_supporters_partials=True
            )
        )

        new_capacity_without_respect_supporters = (
            controller.get_capacity_without_supporters_percentage(
                respect_supporters_partials=False
            )
        )

        old_capacity = controller.get_capacity_without_supporters_percentage()
        
        local = controller.get_local_staff_count(
            include_masters=False
        )
        
        local_with_masters = controller.get_local_staff_count(
            include_masters=True
        )

        print(fac.name)
        print(f"{new_capacity_with_respect_supporters=}")
        print(f"{new_capacity_without_respect_supporters=}")
        print(f"{old_capacity=}")
        print(f"{local=}")
        print(f"{local_with_masters=}")
        print("#" * 50)
