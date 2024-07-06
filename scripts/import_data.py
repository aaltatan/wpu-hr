from .utils import (
    db_import_faculties_specialties,
    db_import_staff,
    db_reset,
)


def run() -> None:
    db_reset()
    db_import_faculties_specialties()
    db_import_staff()
