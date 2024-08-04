from django.db import models

from user.models import User

NULLABLE = {'null': True, 'blank': True}
class Client(models.Model):
    """
    клиенты (получают рассылку) CRUD
    """
    email = models.EmailField(verbose_name="почта", unique=True)
    fio = models.CharField(verbose_name="ФИО", max_length=150)
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return f'{self.fio} ({self.email})'

class Message(models.Model):
    """
    письма CRUD
    """
    subject = models.CharField(max_length=50,verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(User, verbose_name='Владелец', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.subject}'

class Newsletter(models.Model):
    """
    настройки рассылки
    """
    name = models.CharField(max_length=50, verbose_name='Название рассылки', **NULLABLE)
    start_time = models.DateTimeField(verbose_name='время начала отправки рассылки')
    end_time = models.DateTimeField(verbose_name='время окончания отправки рассылки')
    time_last_shipment = models.DateTimeField(verbose_name='время последней отправки сообщения', blank=True, null=True)

    Periodicity = [
        ('daily','раз в день'),
        ('weekly','раз в неделю'),
        ('monthly','раз в месяц')
    ]
    periodicity = models.CharField(max_length=20,verbose_name='периодичность',choices=Periodicity)

    Status = [
        ('finished', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена')
    ]
    status = models.CharField(max_length=20,verbose_name='статус рассылки',choices=Status)

    client = models.ManyToManyField(Client,verbose_name='клиент')
    message = models.ForeignKey(Message,verbose_name='сообщение',on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name='Владелец', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
    def __str__(self):
        return f'Рассылка {self.name}, время: {self.start_time} - {self.end_time}'


class Logs(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название рассылки', default="Рассылка")
    mailing = models.ForeignKey(Newsletter, related_name='attempts', on_delete=models.CASCADE, **NULLABLE)
    attempt_time = models.DateTimeField(verbose_name='дата и время последней попытки')
    attempt = models.CharField(max_length=50, verbose_name='статус попытки')
    comments = models.TextField(max_length=50, verbose_name='Комментарии', **NULLABLE)
    response = models.TextField (verbose_name='ответ почтового сервера', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "лог попыток отправки письма"
        verbose_name_plural = "логи попыток отправки писем"

    def __str__(self):
        return f'{self.attempt_time} - {self.attempt}'