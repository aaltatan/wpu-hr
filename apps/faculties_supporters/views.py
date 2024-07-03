from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.urls import reverse
from django_htmx.http import retarget, HttpResponseLocation
from django.contrib import messages
from .. import messages as msgs
from . import models, forms


def index(request: HttpRequest) -> HttpResponse:
    supporters = models.FacultySupporter.objects.all()
    form = forms.FacultySupporterForm()
    context = {
        'supporters': supporters,
        'instance': supporters.first(),
        'form': form,
    }
    return render(request, 'faculties-supporters/index.html', context)


def get_add_form(request: HttpRequest) -> HttpResponse:
    form = forms.FacultySupporterForm()
    context = {'form': form}
    return render(request, 'faculties-supporters/partials/add-supporter-form.html', context)


@require_POST
def add_supporter(request: HttpRequest) -> HttpResponse:
    form = forms.FacultySupporterForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        return HttpResponseLocation(reverse('supporters-index'))
    else:
        context = {'form': form}
        response = render(request, 'faculties-supporters/partials/add-supporter-form.html', context)
        return retarget(response, '#supporter-form')


@require_http_methods(['DELETE'])
def delete_supporter(request: HttpRequest, id: int) -> HttpResponse:
    supporter = get_object_or_404(models.FacultySupporter, id=id)

    supporter.delete()
    messages.info(request, msgs.MESSAGES['success'], 'success')

    return HttpResponseLocation(reverse('supporters-index'))


def get_update_form(request: HttpRequest, id: int) -> HttpResponse:
    supporter = get_object_or_404(models.FacultySupporter, id=id)
    form = forms.FacultySupporterForm(instance=supporter)
    context = {'form': form, 'supporter': supporter}
    return render(request, 'faculties-supporters/partials/update-supporter-form.html', context)


@require_POST
def update_supporter(request: HttpRequest, id: int) -> HttpResponse:
    supporter = get_object_or_404(models.FacultySupporter, id=id)
    form = forms.FacultySupporterForm(data=request.POST, instance=supporter)

    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        return HttpResponseLocation(reverse('supporters-index'))
    else:
        context = {'form': form, 'supporter': supporter}
        response = render(request, 'faculties-supporters/partials/update-supporter-form.html', context)
        return retarget(response, '#supporter-form')