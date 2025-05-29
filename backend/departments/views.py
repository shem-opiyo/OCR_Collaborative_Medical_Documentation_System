from django.shortcuts import render
from rest_framework import generics
from .models import Department
from .serializers import DepartmentSerializer
from rest_framework.permissions import IsAuthenticated
from employees.models import Employee
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class DepartmentCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            employee = Employee.objects.get(user=self.request.user)
            department = serializer.save(creator=employee)
            department.employees.add(employee)
        except Employee.DoesNotExist:
            raise ValidationError("You must be logged in as an employee to create a department.")

class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_object(self):
        department_id = self.kwargs.get('pk')
        return get_object_or_404(Department, pk=department_id)

class JoinDepartmentView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all() # We'll filter in get_object
    serializer_class = None # We won't be serializing the whole Department

    def get_object(self):
        department_id = self.kwargs.get('pk')
        return get_object_or_404(Department, pk=department_id)

    def update(self, request, *args, **kwargs):
        department = self.get_object()
        employee_id = self.kwargs.get('employee_id')

        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        if employee in department.employees.all():
            return Response({"message": f"{employee.user.username} is already a member of {department.name}."}, status=status.HTTP_200_OK)

        department.employees.add(employee)
        return Response({"message": f"{employee.user.username} has joined {department.name}."}, status=status.HTTP_200_OK)

