from apps.staff import models as staff_models
from apps.faculties import models as faculty_models
from apps.specialties import models as specialties_models
import json
import pandas as pd
import xlwings as xw
from rich import print


def read_initial_data() -> dict[str, dict]:
    """
    read initial data from its json file
    """
    with open('scripts/inputs/initial_data.json', 'r', encoding='utf-8') as file:
      return json.loads(file.read())


def db_reset() -> None:
    """
    delete all records in the database
    """
    staff = staff_models.Staff.objects.all()
    for s in staff:
        s.delete()
        
    specialties = specialties_models.Specialty.objects.all()
    for s in specialties:
      s.delete()
      
    faculties = faculty_models.Faculty.objects.all()
    for f in faculties:
      f.delete()


def db_import_faculties_specialties() -> None:
    """
    import the default faculties and specialties
    """
    initial_data = read_initial_data()
    
    for faculty in initial_data.values():
        name = faculty['name']
        faculty_instance = faculty_models.Faculty.objects.create(name=name)
        
        specialties: list[dict] = faculty['specialties']
        for specialty in specialties:
            specialties_models.Specialty.objects.create(
              faculty=faculty_instance,
              **specialty
            )
    
    print('done importing faculties and specialties! 😁')


def db_import_staff() -> None:
    """
    import staff from staff.xlsx file
    """
    book = xw.Book('scripts/inputs/staff.xlsx')
    sh: xw.Sheet = book.sheets[0]
    lr = sh.range('A10000').end('up').row
    rg = sh.range(f'A2:F{lr}').value
    columns = sh.range(f'A1:F1').value
    
    df = pd.DataFrame(rg, columns=columns)
    data = df.to_dict(orient='records')
    
    initial_data = read_initial_data()
    
    for staff in data:

        faculty_name: str = initial_data[staff['faculty']]['name']
        faculty_instance = (
          faculty_models
          .Faculty
          .objects
          .filter(name=faculty_name)
          .first()
        )
        
        specialty_instance = (
          specialties_models
          .Specialty
          .objects
          .filter(faculty=faculty_instance, name=staff['specialty'])
          .first()
        )
        
        del staff['faculty']
        staff['specialty'] = specialty_instance
        
        staff_models.Staff.objects.create(**staff)
        
    print('done importing staff! 😁')