from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django_htmx.http import retarget
from .. import messages as msgs
from . import models, forms, filters
from rich import print


def index(request: HttpRequest) -> HttpResponse:
    
    form = forms.StaffForm()
    qs = models.Staff.objects.all()
    filtered_staff = filters.StaffFilter(request.GET, queryset=qs)
    
    context = {
        'staff': filtered_staff.qs, 
        'form': form, 
        'filter_form': filtered_staff.form,
        'filtered_total': filtered_staff.qs.count(),
        'total': qs.count(),
    }
    
    return render(request, 'staff/index.html', context)


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
    return HttpResponse('')


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
        context = {'form': add_from, 'stf': staff}
        return render(request, 'staff/partials/table-row.html', context)
    else:
        context = {'form': form, 'stf': staff}
        response = render(request, 'staff/partials/update-staff-form.html', context)
        return retarget(response, '#staff-form')


def toggle_countable(request: HttpRequest, id: int) -> HttpResponse:
    
    staff = get_object_or_404(models.Staff, id=id)
    staff.is_countable = not staff.is_countable
    staff.save()

    messages.info(request, msgs.MESSAGES['success'], 'success')
    
    row_idx = request.headers.get('row-idx')
    context = {'stf': staff, 'row_idx': row_idx}

    return render(request, 'staff/partials/table-row.html', context)
