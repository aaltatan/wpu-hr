from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='base/index.html'
    )

@login_required
def get_messages(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='includes/messages.html'
    )