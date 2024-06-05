from . import serializers, models
from rest_framework import viewsets


class StaffViewSet(viewsets.ModelViewSet):

    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
