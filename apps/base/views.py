from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from ..faculties import models as faculties_models
from ..staff import models as staff_models
from ..base.utils import FacultyController, get_template_data
from .forms import ResultsFilter, CAPACITY_CHOICES, DEFAULT_LOCAL_PERCENTAGE


@login_required
def index(request: HttpRequest) -> HttpResponse:

    filter_from = ResultsFilter()
    form_data: dict = {
        'capacity': CAPACITY_CHOICES[0][0],
        'local_include_masters': False,
        'minimum_local_percentage': DEFAULT_LOCAL_PERCENTAGE,
        'by_student_to_local_teacher_count': True,
    }

    if request.method == 'POST':
        filter_form = ResultsFilter(data=request.POST)
        if filter_form.is_valid():
            form_data = filter_form.cleaned_data
        else:
            context = {'form': filter_form}
            
            response = render(request, 'apps/base/partials/capacity-form.html', context)
            response['Hx-Reselect'] = '#capacity-form'
            response['Hx-Retarget'] = '#capacity-form'
            return response

    faculties_db = faculties_models.Faculty.objects.all()
    faculties: list[dict] = []

    for faculty in faculties_db:
        controller = FacultyController(faculty.pk, staff_models.Time, staff_models.Degree)
        data: dict = get_template_data(form_data, controller, faculty.name)
        faculties.append(data)

    context = {'faculties': faculties, 'form': filter_from}
    response = render(request, 'apps/base/index.html', context)

    if request.htmx:
        response['Hx-Reselect'] = '#results-table'

    return response


@login_required
def get_capacity_form(request: HttpRequest) -> HttpResponse:
    context = {'form': ResultsFilter()}
    return render(request, 'apps/base/partials/capacity-form.html', context)


@login_required
def get_messages(request: HttpRequest) -> HttpResponse:
    return render(request, 'includes/messages.html')