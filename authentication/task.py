import threading
from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, email):
    try:
        task = threading.Thread(
            target=send_mail,
            args=(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
            ),
        )

        task.start()
    except Exception as e:
        print(e)
