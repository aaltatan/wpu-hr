from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django_htmx.http import retarget
from .. import messages as msgs
from . import models, forms, filters


def index(request: HttpRequest) -> HttpResponse:
    
    f = filters.StaffFilter(request.GET, queryset=models.Staff.objects.all())

    form = forms.StaffForm()
    context = {'staff': f.qs, 'form': form, 'filter_form': f.form}
    return render(request, 'staff/index.html', context)


def get_staff_table(request: HttpRequest) -> HttpResponse:

    f = filters.StaffFilter(request.GET, queryset=models.Staff.objects.all())
    context = {'staff': f.qs}
    return render(request, 'staff/partials/staff-table.html', context)


def get_add_form(request: HttpRequest) -> HttpResponse:
    form = forms.StaffForm()
    context = {'form': form}
    return render(request, 'staff/partials/add-staff-form.html', context)


@require_POST
def add_staff(request: HttpRequest) -> HttpResponse:
    form = forms.StaffForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        staff = models.Staff.objects.all()
        context = {'staff': staff}
        return render(request, 'staff/partials/staff-table.html', context)
    else:
        context = {'form': form}
        response = render(request, 'staff/partials/add-staff-form.html', context)
        return retarget(response, '#staff-form')


@require_http_methods(['DELETE'])
def delete_staff(request: HttpRequest, id: int) -> HttpResponse:
    staff = get_object_or_404(models.Staff, id=id)
    staff.delete()
    messages.info(request, msgs.MESSAGES['success'], 'success')
    return render(request, 'includes/messages.html')


def get_update_form(request: HttpRequest, id: int) -> HttpResponse:
    staff = get_object_or_404(models.Staff, id=id)
    form = forms.StaffForm(instance=staff)
    context = {'form': form, 'stf': staff}
    return render(request, 'staff/partials/update-staff-form.html', context)


@require_POST
def update_staff(request: HttpRequest, id: int) -> HttpResponse:
    staff = get_object_or_404(models.Staff, id=id)
    form = forms.StaffForm(data=request.POST, instance=staff)

    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        add_from = forms.StaffForm()
        staff = models.Staff.objects.all()
        context = {'form': add_from, 'staff': staff}
        return render(request, 'staff/partials/staff-table.html', context)
    else:
        context = {'form': form, 'stf': staff}
        response = render(request, 'staff/partials/update-staff-form.html', context)
        return retarget(response, '#staff-form')


def toggle_countable(request: HttpRequest, id: int) -> HttpResponse:
    
    staff = get_object_or_404(models.Staff, id=id)
    staff.is_countable = not staff.is_countable
    staff.save()

    print(request.GET)
    print("#" * 100)

    messages.info(request, msgs.MESSAGES['success'], 'success')

    staff = models.Staff.objects.all()

    return redirect(reverse('staff-table'))
