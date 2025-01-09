from celery import shared_task
from datetime import datetime
from datetime import timedelta
from .models import Reminder
from django.core.mail import send_mail
from .utilities import selecting_messaging_type

@shared_task
def test_task():
    print(f"Test task executed at: {datetime.now()}")


@shared_task
def send_reminder_notification():
    now = datetime.now()
    reminders = Reminder.objects.filter(reminder_date__lte=now, is_shortlisted=False, is_rejected=False)
    if reminders.exists():
        print("-------------- sending the notification ------------------------------")
        for reminder in reminders:
            message = selecting_messaging_type(
                reminder_type=reminder.reminder_type,
                company_name=reminder.job_application.company.name,
                position=reminder.job_application.position
                )
            send_mail(
                subject="Reminder Notification",
                message=message,
                from_email="suhailpk2427@gmail.com",
                recipient_list=[reminder.job_application.user.email],
            )
            status_list = ["AP", "AA", "SA", "NS"]

    
             # Find the next status
            if reminder.reminder_type in status_list:
                current_index = status_list.index(reminder.reminder_type)
                if reminder.reminder_type == "NS":  # Special condition for the last element
                    next_status = "NS"
                else:
                    next_index = (current_index + 1) % len(status_list)  # Wrap around using modulo
                    next_status = status_list[next_index]
            else:
                return "Invalid status.", None


            reminder.reminder_date = now + timedelta(days=7)
            if reminder.reminder_type == "NS":
                reminder.is_rejected = True
            reminder.reminder_type = next_status
            reminder.save()
    else:
        print("----------------- not users found for sending notification --------------------")


