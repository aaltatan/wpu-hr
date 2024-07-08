from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from ..faculties import models as faculties_models
from ..staff import models as staff_models
from ..base.utils import FacultyController
from .forms import ResultsFilter


@login_required
def index(request: HttpRequest) -> HttpResponse:

    faculties_db = faculties_models.Faculty.objects.all()
    faculties: list[dict] = []
    
    if request.htmx:
        filter_form = ResultsFilter(data=request.GET)
    
        if filter_form.is_valid():
        
            filters = filter_form.cleaned_data
        
            for faculty in faculties_db:
                
                data: dict = {}

                controller = FacultyController(faculty, staff_models.Time, staff_models.Degree)
                
                data['name'] = faculty.name
                
                if filters['capacity'] == 'respect_each_specialty_fulltime_parttime_percentage': 
                    data['capacity'] = (
                        controller.get_capacity_without_supporters_percentage()
                    )
                elif filters['capacity'] == 'calculate_all_specialties_as_one':
                    data['capacity'] = (
                        controller.get_capacity_without_supporters_percentage(
                            respect_supporters_partials=False
                        )
                    )
                else:
                    data['capacity'] = controller.get_capacity_with_supporters_percentage()
                
                data['local'] = controller.get_local_staff_count(
                    include_masters=filters['local_include_masters'],
                )
                data['required_local'] = controller.get_required_local_teachers_count(
                    50
                )
                data['students_count'] = controller.students_count
                
                faculties.append(data)
        else:
            
            context = {'form': filter_form}
            return render(request, 'apps/base/index.html', context)
        
    else:
        filter_form = ResultsFilter()
        
    context = {'faculties': faculties, 'form': filter_form}
    return render(request, 'apps/base/index.html', context)


@login_required
def get_capacity_form(request: HttpRequest) -> HttpResponse:
    form = ResultsFilter()
    context = {'form': form}
    return render(request, 'apps/base/partials/capacity-form.html', context)


@login_required
def get_messages(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='includes/messages.html'
    )