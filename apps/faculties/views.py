from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.urls import reverse
from django_htmx.http import retarget, HttpResponseLocation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .. import messages as msgs
from . import models, forms


@login_required
def index(request: HttpRequest) -> HttpResponse:
    faculties = models.Faculty.objects.all()
    form = forms.FacultyForm()
    context = {
        'faculties': faculties,
        'instance': faculties.first(),
        'form': form,
    }
    return render(request, 'faculties/index.html', context)


@login_required
def get_add_form(request: HttpRequest) -> HttpResponse:
    form = forms.FacultyForm()
    context = {'form': form}
    return render(request, 'faculties/partials/add-faculty-form.html', context)


@login_required
@require_POST
def add_faculty(request: HttpRequest) -> HttpResponse:
    form = forms.FacultyForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        return HttpResponseLocation(reverse('faculties-index'))
    else:
        context = {'form': form}
        response = render(request, 'faculties/partials/add-faculty-form.html', context)
        return retarget(response, '#faculty-form')


@login_required
@require_http_methods(['DELETE'])
def delete_faculty(request: HttpRequest, id: int) -> HttpResponse:
    
    faculty = get_object_or_404(models.Faculty, id=id)

    if faculty.specialties.count():
        messages.info(request, msgs.MESSAGES['cannot_delete_faculty'], 'danger')
    else:
        faculty.delete()
        messages.info(request, msgs.MESSAGES['success'], 'success')

    return HttpResponseLocation(reverse('faculties-index'))


@login_required
def get_update_form(request: HttpRequest, id: int) -> HttpResponse:
    faculty = get_object_or_404(models.Faculty, id=id)
    form = forms.FacultyForm(instance=faculty)
    context = {'form': form, 'faculty': faculty}
    return render(request, 'faculties/partials/update-faculty-form.html', context)


@login_required
@require_POST
def update_faculty(request: HttpRequest, id: int) -> HttpResponse:
    faculty = get_object_or_404(models.Faculty, id=id)
    form = forms.FacultyForm(data=request.POST, instance=faculty)

    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        return HttpResponseLocation(reverse('faculties-index'))
    else:
        context = {'form': form, 'faculty': faculty}
        response = render(request, 'faculties/partials/update-faculty-form.html', context)
        return retarget(response, '#faculty-form')