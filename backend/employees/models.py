from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Employee(models.Model):
    ROLE_CHOICES = [
        ('DOC', 'Doctor'),
        ('NUR', 'Nurse'),
        ('ADM', 'Administrator'),
        ('LAB', 'Lab Technician'),
    ]

    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    patients      = models.ManyToManyField('patients.Patient', blank=True, related_name='assigned_employees')
    role          = models.CharField(max_length=3, choices=ROLE_CHOICES)
    department    = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name="new_member")
    contact_info  = models.CharField(max_length=100)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"
