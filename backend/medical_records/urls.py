from django.urls import path
from .views import *

urlpatterns = [
    path('create/', MedicalRecordCreateView.as_view(), name='medical-record-create'),
    path('get-record/<int:record_id>/', MedicalRecordRetrieveView.as_view(), name='medical-record-list'),
    path('<int:pk>/delete/', MedicalRecordDeleteView.as_view(), name='medical-record-delete'),
    path('<int:pk>/update/', MedicalRecordUpdateView.as_view(), name='medical-record-update'),
    path('patient/<int:patient_id>/get-records/', PatientMedicalRecordsView.as_view(), name='patient-medical-records'),
    path('employee/accessible-records/', EmployeeAccessibleRecordsView.as_view(), name='employee-accessible-records'),
]
