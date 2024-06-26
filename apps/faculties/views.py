from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django_htmx.http import retarget
from django.contrib import messages
from .. import messages as msgs
from . import models, forms


def index(request: HttpRequest) -> HttpResponse:
    faculties = models.Faculty.objects.all()
    form = forms.FacultyForm()
    context = {
        'faculties': faculties,
        'form': form,
    }
    return render(request, 'faculties/index.html', context)


def get_add_form(request: HttpRequest) -> HttpResponse:
    form = forms.FacultyForm()
    context = {'form': form}
    return render(request, 'faculties/partials/add-faculty-form.html', context)


@require_POST
def add_faculty(request: HttpRequest) -> HttpResponse:
    form = forms.FacultyForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        faculties = models.Faculty.objects.all()
        context = {'faculties': faculties}
        return render(request, 'faculties/partials/faculties-table.html', context)
    else:
        context = {'form': form}
        response = render(request, 'faculties/partials/add-faculty-form.html', context)
        return retarget(response, '#faculty-form')


@require_http_methods(['DELETE'])
def delete_faculty(request: HttpRequest, id: int) -> HttpResponse:
    faculty = get_object_or_404(models.Faculty, id=id)

    if faculty.staff.count():
        messages.info(request, msgs.MESSAGES['cannot_delete'], 'danger')
        faculties = models.Faculty.objects.all()
        context = {'faculties': faculties}
        response = render(request, 'faculties/partials/faculties-table.html', context)
        return retarget(response, '#faculties-table')
    else:
        faculty.delete()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        return render(request, 'includes/messages.html')


def get_update_form(request: HttpRequest, id: int) -> HttpResponse:
    faculty = get_object_or_404(models.Faculty, id=id)
    form = forms.FacultyForm(instance=faculty)
    context = {'form': form, 'faculty': faculty}
    return render(request, 'faculties/partials/update-faculty-form.html', context)


@require_POST
def update_faculty(request: HttpRequest, id: int) -> HttpResponse:
    faculty = get_object_or_404(models.Faculty, id=id)
    form = forms.FacultyForm(data=request.POST, instance=faculty)

    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        add_from = forms.FacultyForm()
        faculties = models.Faculty.objects.all()
        context = {'form': add_from, 'faculties': faculties}
        return render(request, 'faculties/partials/faculties-table.html', context)
    else:
        context = {'form': form, 'faculty': faculty}
        response = render(request, 'faculties/partials/update-faculty-form.html', context)
        return retarget(response, '#faculty-form')
