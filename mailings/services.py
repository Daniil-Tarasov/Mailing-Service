from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailings.models import Mailing


def send_mailing(mailing):

    mailing.status = Mailing.LAUNCHED
    mailing.date_of_first_sending = timezone.now()
    mailing.save()

    recipients = mailing.recipients.all()
    message = mailing.message

    subject = message.subject
    body = message.message

    for recipient in recipients:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [recipient.email],
            fail_silently=False,
        )

    mailing.date_of_sending_end = timezone.now()
    mailing.status = Mailing.COMPLETED
    mailing.save()
