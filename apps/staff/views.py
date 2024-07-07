from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django_htmx.http import retarget, HttpResponseLocation
from .. import messages as msgs
from . import models, forms, filters
import json


PART: str = 'apps/staff/partials/'


@login_required
def index(request: HttpRequest) -> HttpResponse:
        
    form = forms.StaffForm()
    qs = (
        models
        .Staff
        .objects
        .select_related(
            'specialty', 
            'specialty__faculty', 
        ).all()
    )
    
    filtered_staff = filters.StaffFilter(request.GET, queryset=qs)
    
    paginator = Paginator(filtered_staff.qs, 10)
    
    page = int(request.GET.get('page', 1))
    page_obj = paginator.get_page(page)
    
    if page > page_obj.paginator.num_pages:
        page_obj = paginator.get_page(page_obj.paginator.num_pages)
    
    next_page = page_obj.next_page_number() if page_obj.has_next() else page - 1
    last_page = page_obj.paginator.num_pages
    previous_page = page_obj.previous_page_number() if page_obj.has_previous() else 1
    
    context = {
        'staff': page_obj, 
        'instance': filtered_staff.qs.first(), 
        'form': form, 
        'filter_form': filtered_staff.form,
        'filtered_total': filtered_staff.qs.count(),
        'total': qs.count(),
        'params_next': json.dumps({**request.GET, 'page': next_page}),
        'params_last': json.dumps({**request.GET, 'page': last_page}),
        'params_previous': json.dumps({**request.GET, 'page': previous_page}),
        'params_first': json.dumps({**request.GET, 'page': 1}),
    }
    
    return render(request, 'apps/staff/index.html', context)


@login_required
def get_add_form(request: HttpRequest) -> HttpResponse:
    form = forms.StaffForm()
    context = {'form': form}
    return render(request, PART + 'add-staff-form.html', context)


@login_required
@require_POST
def add_staff(request: HttpRequest) -> HttpResponse:
    form = forms.StaffForm(request.POST)
    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        return HttpResponseLocation(reverse('staff-index'))
    else:
        context = {'form': form}
        response = render(request, PART + 'add-staff-form.html', context)
        return retarget(response, '#staff-form')


@login_required
@require_http_methods(['DELETE'])
def delete_staff(request: HttpRequest, id: int) -> HttpResponse:
    staff = get_object_or_404(models.Staff, id=id)
    staff.delete()
    messages.info(request, msgs.MESSAGES['success'], 'success')
    return HttpResponse('')


@login_required
def get_update_form(request: HttpRequest, id: int) -> HttpResponse:
    staff = get_object_or_404(models.Staff, id=id)
    form = forms.StaffForm(instance=staff)
    context = {'form': form, 'stf': staff}
    return render(request, PART + 'update-staff-form.html', context)


@login_required
@require_POST
def update_staff(request: HttpRequest, id: int) -> HttpResponse:
    staff = get_object_or_404(models.Staff, id=id)
    form = forms.StaffForm(data=request.POST, instance=staff)

    if form.is_valid():
        form.save()
        messages.info(request, msgs.MESSAGES['success'], 'success')
        add_from = forms.StaffForm()
        context = {'form': add_from, 'stf': staff}
        return render(request, PART + 'table-row.html', context)
    else:
        context = {'form': form, 'stf': staff}
        response = render(request, PART + 'update-staff-form.html', context)
        return retarget(response, '#staff-form')


@login_required
def toggle_countable(request: HttpRequest, id: int) -> HttpResponse:
    
    staff = get_object_or_404(models.Staff, id=id)
    staff.is_countable = not staff.is_countable
    staff.save()

    row_idx = request.headers.get('row-idx')
    context = {'stf': staff, 'row_idx': row_idx}

    return render(request, PART + 'table-row.html', context)
