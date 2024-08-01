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

    # send_emails('a')


def sorted_mailings():
    """
    Проверка статусов рассылки на актуальность
    """
    time_zone = pytz.timezone(settings.TIME_ZONE)
    time_now = datetime.now(time_zone)
    mailings = Newsletter.objects.filter(status__in=['created', 'launched'])
    # print(mailings)
    if len(mailings) > 0:
        for mailing in mailings:
            if mailing.status == 'created' and mailing.start_time <= time_now:
                mailing.status = 'launched'
                mailing.save()
            elif mailing.status == 'launched' and mailing.end_time <= time_now:
                mailing.status = 'finished'
                mailing.save()

            # print(mailing.start_time)
            # print(mailing.start_time + timezone.timedelta(days = 1))
            # print(mailing.start_time + timezone.timedelta(weeks = 1))
            # print(mailing.start_time + timedelta(month = 1))

    # print(mailings)
    # print()

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


            # print(mailing)
            # print()

def send_emails(mailing):
    """
    Отправка письма
    """
    number_clients = 0    # количество клиетов
    sent_successfully = 0    # количество успешно отправленных соощений
    response = []    # ответ сервера

    # mailings = Newsletter.objects.filter(status='finished')
    # mailing = mailings[0]

    # message = Message.objects.filter(id=mailing.message_id)
    # message = message[0]

    message = mailing.message
    # print(m)
    # print(m.body)


    # emails = []
    clients = mailing.client.all()
    for client in clients:
        number_clients += 1
        # client.email
    # print(emails)



    # client = Client.objects.filter(id=client.id)
    # print(client)

        try:
            send_mail(
                subject=message.subject,  # тема письма
                message=message.body,  # сообщение
                from_email=EMAIL_HOST_USER,  # с какого мейла отправляем
                recipient_list=[client.email],  # список имейлов на которые отправляем
                fail_silently = False,
            )
            sent_successfully += 1
            response.append(str(send_mail))

            # print(send_mail)
        except SMTPException as e:
            response.append(str(e))
        #     print('Ошибка при отправке письма')
        #     print(e)
        #
        # print()
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
        response=f'{'\n'.join(response)}'
    )
    # print(response)



    # MailingAttempt.objects.create(
    #     mailing=mailing,
    #     status=status,
    #     server_response=server_response,
    #     client_email=client.email








        # print(mailing)














        # recipients = mailing.clients.all()
        # subject = mailing.message.subject
        # body = mailing.message.body
        # for recipient in recipients:
        #     try:
        #         send_email(recipient.email, subject, body)
        #     except Exception as e:
        #         print(f'Ошибка при отправке письма для {recipient.email}: {e}')












    # #нынешнее время
    # time_zone = pytz.timezone(settings.TIME_ZONE)
    # now = datetime.now(time_zone)
    # print(now)







    # posts = Newsletter.objects.all()
    # print(posts)
    # print()
    #
    # for i in posts:
    #     i.periodicity = 'раз в месяц'
    #     i.save()
    #
    # print(posts)
    # print()
    # print()
    # print()




    # time_zone = pytz.timezone(settings.TIME_ZONE)
    # now = datetime.now(time_zone)
    # print(now)



    #




    # print(timezone)
    # print()
    # print(now + timezone.timedelta(days=1))