from django.urls import path
from .views import *

urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('list/', EmployeeListView.as_view(), name='employee-list'),
    path('delete/<int:id>/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('find/<int:id>/', EmployeeSearchView.as_view(), name='employee-find'),
    path('me/', MeView.as_view(), name='employee-me'),
    path('<int:employee_id>/add-patient/<int:patient_id>/', AddPatientToEmployeeView.as_view(), name='add-patient-to-employee'),
    path('<int:employee_id>/my-patients/', EmployeePatientListView.as_view(), name='employee-patients-list'),
    path('<int:employee_id>/my-departments/', EmployeeDepartmentsViewList.as_view(), name='employee-department-list'),
    path('authorize-employee/user/<int:user_id>/', AuthorizeUserAsEmployeeView.as_view(), name='authorize-employee'),
]
