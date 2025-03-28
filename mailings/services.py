import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailings.models import Mailing, MailingAttempts


def send_mailing(mailing):
    mailing.status = Mailing.LAUNCHED
    mailing.date_of_first_sending = timezone.now()
    mailing.save()

    attempt, create = MailingAttempts.objects.get_or_create(
        mailing=mailing,
        defaults={'status': MailingAttempts.not_successfully}
    )

    try:
        message = mailing.message
        subject = message.subject
        body = message.message

        for recipient in mailing.recipients.all():
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.email],
                fail_silently=False,
            )

        attempt.status = MailingAttempts.successfully
        mailing.status = Mailing.COMPLETED

    except smtplib.SMTPException as e:
        attempt.mail_server_response = f"Ошибка SMTP: {str(e)}"

    except Exception as e:
        attempt.mail_server_response = f"Системная ошибка: {str(e)}"

    finally:
        attempt.save()
        mailing.date_of_sending_end = timezone.now()
        mailing.save()
