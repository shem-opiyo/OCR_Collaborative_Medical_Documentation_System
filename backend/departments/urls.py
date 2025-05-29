from django.urls import path
from .views import *

urlpatterns = [
    path('create/', DepartmentCreateView.as_view(), name='department-create'),
    path('list/', DepartmentListView.as_view(), name='department-list'),
    path('get-department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('<int:pk>/join/<int:employee_id>/', JoinDepartmentView.as_view(), name='department-join'),

]
