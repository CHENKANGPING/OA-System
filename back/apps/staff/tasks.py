from HiiaenOAback import celery_app
from django.core.mail import send_mail
from django.conf import settings


@celery_app.task(name='send_email_task')
def send_email_task(email, subject, message):
    send_mail(subject, recipient_list=[email], message=message,
              from_email=settings.DEFAULT_FROM_EMAIL)

