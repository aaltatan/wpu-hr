from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets
from . import models, serializers

def index(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='index.html'
    )


class FacultyViewSet(viewsets.ModelViewSet):
    
    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer

    
