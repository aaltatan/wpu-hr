from rest_framework import serializers
from . import models


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Staff
        fields = "__all__"