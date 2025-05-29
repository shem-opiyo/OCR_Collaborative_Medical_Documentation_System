from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'name', 'date_of_birth', 'gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'patient_id')
    list_filter = ('gender', 'created_at')
    # You can customize the admin interface further here