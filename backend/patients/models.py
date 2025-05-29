from django.db import models

# Create your models here.

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    patient_id          = models.AutoField(primary_key=True)
    name                = models.CharField(max_length=200)
    date_of_birth       = models.DateField()
    gender              = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone      = models.CharField(max_length=100)
    created_at          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (ID: {self.patient_id})"
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['created_at']
        # You can add more options here if needed
