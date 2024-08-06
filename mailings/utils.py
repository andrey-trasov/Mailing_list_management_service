from datetime import datetime
from smtplib import SMTPException

import pytz
from django.conf import settings

from mailings.models import Newsletter, Logs
from django.utils import timezone

from django.core.mail import send_mail
from myproject.settings import EMAIL_HOST_USER

def send_mailing():
    """
    :return:
    """
    sorted_mailings()    # Проверка статусов рассылки на актуальность
    checking_date()    # Отправка писем



def sorted_mailings():
    """
    Проверка статусов рассылки на актуальность
    """
    time_zone = pytz.timezone(settings.TIME_ZONE)
    time_now = datetime.now(time_zone)
    mailings = Newsletter.objects.filter(status__in=['created', 'launched'])
    if len(mailings) > 0:
        for mailing in mailings:
            if mailing.status == 'created' and mailing.start_time <= time_now:
                mailing.status = 'launched'
                mailing.save()
            elif mailing.status == 'launched' and mailing.end_time <= time_now:
                mailing.status = 'finished'
                mailing.save()

def checking_date():
    """
    Отправка писем
    """
    time_zone = pytz.timezone(settings.TIME_ZONE)
    time_now = datetime.now(time_zone)
    mailings = Newsletter.objects.filter(status='launched')
    for mailing in mailings:
        #Проверяем количество дней для новой отправки
        if mailing.periodicity == 'daily':
            days = 1
        elif mailing.periodicity == 'weekly':
            days = 7
        elif mailing.periodicity == 'monthly':
            days = 30
        #Если пришло время отправлять сообщение (отправений сообщений еще не было, или пришло время отправки)
        if mailing.time_last_shipment == None or mailing.time_last_shipment + timezone.timedelta(days=days) <= time_now:
            mailing.time_last_shipment = time_now
            mailing.save()
            send_emails(mailing)    # передаем 1 рассылку для отправки сообщений


def send_emails(mailing):
    """
    Отправка письма
    """
    number_clients = 0    # количество клиетов
    sent_successfully = 0    # количество успешно отправленных соощений
    response = []    # ответ сервера

    message = mailing.message

    clients = mailing.client.all()
    for client in clients:
        number_clients += 1

        try:
            send_mail(
                subject=message.subject,  # тема письма
                message=message.body,  # сообщение
                from_email=EMAIL_HOST_USER,  # с какого мейла отправляем
                recipient_list=[client.email],  # список имейлов на которые отправляем
                fail_silently = False,
            )
            sent_successfully += 1
            # response.append(str(send_mail))


        except SMTPException as e:
            response.append(str(e))

    logs(mailing, number_clients, sent_successfully, response)

def logs(mailing, number_clients, sent_successfully, response):

    time_zone = pytz.timezone(settings.TIME_ZONE)
    time_now = datetime.now(time_zone)    #время отправки
    # высчитываем статус рассылки
    if number_clients > 0 and sent_successfully > 0 and number_clients / sent_successfully <= 2:
        status = 'успешно'    #доставлено более 50% клиентам

    else:
        status = 'не успешно'

    if len(response) == 0:
        response.append('Нет ответа от сервера')

    Logs.objects.create(
        name=mailing.name,
        mailing=mailing,
        attempt_time=time_now,
        attempt=status,
        comments=f'Успешно доставлено {sent_successfully} клиентам из {number_clients}',
        response=f'{'\n'.join(response)}',
        owner=mailing.owner
    )
