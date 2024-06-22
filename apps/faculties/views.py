from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from . import models, forms


def index(request: HttpRequest) -> HttpResponse:

    faculties = models.Faculty.objects.all()
    form = forms.FacultyForm()

    context = {
        'faculties': faculties,
        'form': form,
    }

    return render(request, 'faculties/index.html', context)
