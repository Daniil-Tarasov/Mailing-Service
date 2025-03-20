from django.db import models

class MailingRecipient(models.Model):
    email = models.CharField(max_length=100, unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['email']

class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['subject']

class Mailing(models.Model):
    CREATED = 'Создана'
    LAUNCHED = 'Запущена'
    COMPLETED = 'Завершена'
    STATUS_MAILING = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    date_of_first_sending = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время первой отправки")
    date_of_sending_end = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=10, choices=STATUS_MAILING, default=CREATED, verbose_name="Статус")
    message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        related_name="mailing",
        null=True,
        blank=True,
        verbose_name="Сообщение"
    )
    recipients = models.ManyToManyField(
        'MailingRecipient',
        related_name='mailing',
        verbose_name="Получатель"
    )

    def __str__(self):
        return f'{self.recipients} - {self.message}: {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['status']
