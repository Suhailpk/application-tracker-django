from django.db import models
from django.contrib.auth.hashers import make_password
from django.conf import settings

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    date_of_birth = models.DateField(null=True, blank=True)


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('AP', 'Applied'),
        ('IN', 'Interview'),
        ('OF', 'Offer'),
        ('RE', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AP')
    date_applied = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.position
