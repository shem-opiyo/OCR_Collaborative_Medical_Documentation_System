from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db.models import Q
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from employees.models import Employee
from patients.models import Patient


class MedicalRecordCreateView(generics.CreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            raise PermissionDenied("Employee profile not found.")
        serializer.save(staff=employee)  # auto-assign creator

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data['record_id'] = serializer.instance.pk
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class HasRecordAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            raise PermissionDenied("Employee profile not found.")

        return (
            obj.staff == employee or
            employee in obj.staff_access.all() or
            obj.departments.filter(id__in=employee.departments.values_list('id', flat=True)).exists()
        )


class MedicalRecordDeleteView(generics.DestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            raise PermissionDenied("Employee profile not found.")
        if instance.staff != employee:
            raise PermissionDenied("Only the creator can delete this record.")
        instance.delete()


class MedicalRecordUpdateView(generics.UpdateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, HasRecordAccess]
    lookup_field = 'pk'


class PatientMedicalRecordsView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            raise PermissionDenied("Patient does not exist.")
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            raise PermissionDenied("Employee profile not found.")

        return MedicalRecord.objects.filter(
            patient=patient
        ).filter(
            Q(staff=employee) |
            Q(staff_access=employee) |
            Q(departments__in=employee.departments.all())
        ).distinct()


class MedicalRecordRetrieveView(generics.RetrieveAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'record_id'

    def get_object(self):
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            raise PermissionDenied("Employee profile not found.")

        record_id = self.kwargs.get('record_id')
        if not record_id:
            raise NotFound("Record ID not provided.")

        try:
            record = MedicalRecord.objects.get(pk=record_id)
        except MedicalRecord.DoesNotExist:
            raise NotFound("Medical record not found.")

        if not (
            record.staff == employee or
            employee in record.staff_access.all() or
            record.departments.filter(id__in=employee.departments.values_list('id', flat=True)).exists()
        ):
            raise PermissionDenied("You do not have permission to access this record.")

        return record


class EmployeeAccessibleRecordsView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            employee = Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            raise PermissionDenied("Employee profile not found.")

        return MedicalRecord.objects.filter(
            Q(staff=employee) |
            Q(staff_access=employee) |
            Q(departments__in=employee.departments.all())
        ).distinct()
