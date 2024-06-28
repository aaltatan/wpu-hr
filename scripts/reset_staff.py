from apps.staff import models as staff_models
from apps.faculties import models as faculty_models
import pandas as pd
import xlwings as xw
from rich import print


def run() -> None:
    book = xw.Book('scripts/inputs/staff.xlsx')
    sh: xw.Sheet = book.sheets[0]
    lr = sh.range('A10000').end('up').row
    rg = sh.range(f'A2:F{lr}').value
    columns = sh.range(f'A1:F1').value
    
    faculty_dict: dict[str, str] = {
      'Architecture': 'هندسة العمارة والتخطيط العمراني',
      'Civil': 'الهندسة المدنية',
      'Dentistry': 'طب الأسنان',
      'Engineering': 'الهندسة المعلوماتية',
      'Management': 'العلوم الإدارية والمالية',
      'Pharmacy': 'الصيدلة',
    }
    
    staff = staff_models.Staff.objects.all()
    for s in staff:
        s.delete()
    
    df = pd.DataFrame(rg, columns=columns)
    data = df.to_dict(orient='records')
    
    for row in data:
        row['faculty'] = (
          faculty_models
          .Faculty
          .objects
          .filter(name=faculty_dict[row['faculty']])
          .first()
        )
        
        staff_instance = staff_models.Staff(**row)
        staff_instance.save()
        
        
    print('done importing!')