from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='base/index.html'
    )


def get_messages(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='includes/messages.html'
    )