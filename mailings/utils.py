from django.core.mail import send_mail
from myproject.settings import EMAIL_HOST_USER



def sending_message():
    """
    ОТправляет сообщение
    """
    send_mail(
               subject = 'Подтверждение почты',    #тема письма
               message = f'Перейди по ссылке для подтверждения почты',    #сообщение
               from_email = EMAIL_HOST_USER,    #с какого мейла отправляем
               recipient_list = ['py.te.1@mail.ru', 'py.te.2@mail.ru', 'py.te.3@mail.ru']    #список имейлов на которые отправляем
    )
