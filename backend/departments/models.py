# employees/models.py
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, related_name="created_departments")
    created_at = models.DateTimeField(auto_now_add=True)
    employees = models.ManyToManyField('employees.Employee', blank=True, related_name="departments")

    def __str__(self):
        return self.name

