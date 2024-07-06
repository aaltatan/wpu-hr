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
    specialties = models.Specialty.objects.select_related('faculty').all()
    form = forms.SpecialtyForm()
    context = {
        'specialties': specialties,
        'instance': specialties.first(),
        'form': form,
    }
    return render(request, 'specialties/index.html', context)


@login_required
def get_add_form(request: HttpRequest) -> HttpResponse:
    form = forms.SpecialtyForm()
    context = {'form': form}
    return render(request, 'specialties/partials/add-specialty-form.html', context)


@login_required
@require_POST
def add_specialty(request: HttpRequest) -> HttpResponse:
    form = forms.SpecialtyForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        return HttpResponseLocation(reverse('specialties-index'))
    else:
        context = {'form': form}
        response = render(request, 'specialties/partials/add-specialty-form.html', context)
        return retarget(response, '#specialty-form')


@login_required
@require_http_methods(['DELETE'])
def delete_specialty(request: HttpRequest, id: int) -> HttpResponse:
    specialty = get_object_or_404(models.Specialty, id=id)

    if specialty.staff.count():
        messages.info(request, msgs.MESSAGES['cannot_delete_specialty'], 'danger')
    else:
        messages.info(request, msgs.MESSAGES['success'], 'success')
        specialty.delete()

    return HttpResponseLocation(reverse('specialties-index'))


@login_required
def get_update_form(request: HttpRequest, id: int) -> HttpResponse:
    specialty = get_object_or_404(models.Specialty, id=id)
    form = forms.SpecialtyForm(instance=specialty)
    context = {'form': form, 'specialty': specialty}
    return render(request, 'specialties/partials/update-specialty-form.html', context)


@login_required
@require_POST
def update_specialty(request: HttpRequest, id: int) -> HttpResponse:
    specialty = get_object_or_404(models.Specialty, id=id)
    form = forms.SpecialtyForm(data=request.POST, instance=specialty)

    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        return HttpResponseLocation(reverse('specialties-index'))
    else:
        context = {'form': form, 'specialty': specialty}
        response = render(request, 'specialties/partials/update-specialty-form.html', context)
        return retarget(response, '#specialty-form')