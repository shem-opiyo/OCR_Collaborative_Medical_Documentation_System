from django.urls import path
from .views import *

urlpatterns = [
    path('create/', PatientCreateView.as_view(), name='patient-create'),
    path('list/', PatientListView.as_view(), name='patient-list'),
    path('find/<int:patient_id>/', PatientSearchView.as_view(), name='patient-find'),
    path('update/<int:pk>/', UpdatePatientView.as_view(), name='patient-update'),
    path('delete/<int:pk>/', PatientDeleteView.as_view(), name='patient-delete'),

]