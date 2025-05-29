from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['pk', 'name', 'date_of_birth', 'phone']
        read_only_fields = ['pk']
