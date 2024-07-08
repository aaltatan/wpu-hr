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
    filter_form = ResultsFilter(data=request.GET)
    faculties: list[dict] = []
    
    if filter_form.is_valid():
    
        filters = filter_form.cleaned_data
    
        for faculty in faculties_db:
            
            data: dict = {}

            controller = FacultyController(faculty, staff_models.Time, staff_models.Degree)
            
            data['name'] = faculty.name
            
            if filters['capacity'] == 'new_with_supporters_percentage': 
                data['capacity'] = (
                    controller.get_capacity_without_supporters_percentage()
                )
            elif filters['capacity'] == 'new_without_supporters_percentage':
                data['capacity'] = (
                    controller.get_capacity_without_supporters_percentage(
                        respect_supporters_partials=False
                    )
                )
            else:
                data['capacity'] = controller.get_capacity_with_supporters_percentage()
            
            data['local'] = controller.get_local_staff_count(
                include_masters=filters['local_include_masters']
            )
            data['required_local'] = controller.get_required_local_teachers_count()
            data['students_count'] = controller.students_count
            
            faculties.append(data)
        
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