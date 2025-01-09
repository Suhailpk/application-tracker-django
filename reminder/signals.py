from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
from .models import Reminder

@receiver(pre_save, sender=Reminder)
def set_reminder_date_pre_save(sender, instance, **kwargs):
    if not instance.reminder_date:  # Only set if reminder_date is not provided
        instance.reminder_date = now() + timedelta(days=7)
