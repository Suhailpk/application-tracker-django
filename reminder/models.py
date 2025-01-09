from django.db import models
from api.models import JobApplication
from django.conf import settings

# Create your models here.
class Reminder(models.Model):

    STATUS_CHOICES = [
        ('AP', 'Applied'),
        ('AA', 'Actively Applying'),
        ('SA', 'Still Applying'),
        ('NS', 'Not Selected'),
    ]

    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_date = models.DateTimeField()
    message = models.TextField(null=True, blank=True)
    reminder_type = models.CharField(max_length=50, choices=STATUS_CHOICES, default='AP')
    is_shortlisted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.job_application} - {self.reminder_date}"