from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, recipient, from_email=settings.DEFAULT_FROM_EMAIL):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[recipient],
        fail_silently=False,
    )
