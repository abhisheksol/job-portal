# auth_app/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_application_status_email(user_email, subject, message):
    send_mail(
        subject,
        message,
        'abhisheksolapure2003@gmail.com',  # from
        [user_email],                       # to
        fail_silently=False,
    )
