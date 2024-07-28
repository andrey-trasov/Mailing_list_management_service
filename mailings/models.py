from django.db import models


NULLABLE = {'null': True, 'blank': True}
class Client(models.Model):
    """
    клиенты (получают рассылку) CRUD
    """
    email = models.EmailField(verbose_name="почта", unique=True)
    fio = models.CharField(verbose_name="ФИО", max_length=150)
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)

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


    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.subject}'

class Newsletter(models.Model):
    """
    настройки рассылки
    """
    start_time = models.DateTimeField(verbose_name='время начала отправки рассылки')
    end_time = models.DateTimeField(verbose_name='время окончания отправки рассылки')
    time_last_shipment = models.DateTimeField(verbose_name='время последней отправки сообщения', blank=True, null=True)

    daily = 'раз в день'
    weekly = 'раз в неделю'
    monthly = 'раз в месяц'
    Periodicity = [
        (daily,'раз в день'),(weekly,'раз в неделю'),(monthly,'раз в месяц')
    ]
    periodicity = models.CharField(max_length=20,verbose_name='периодичность',choices=Periodicity)

    finished = 'завершена'
    created = 'создана'
    launched = 'запущена'
    Status = [
        (finished, 'завершена'), (created, 'создана'), (launched, 'запущена')
    ]
    status = models.CharField(max_length=20,verbose_name='статус рассылки',choices=Status,default=created)

    client = models.ManyToManyField(Client,verbose_name='клиент')
    message = models.ForeignKey(Message,verbose_name='сообщение',on_delete=models.CASCADE)


    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
    def __str__(self):
        return f'Время: {self.start_time} - {self.end_time}, статус рассылки: {self.status}, периодичность рассылки: {self.periodicity}'


class Logs(models.Model):
    attempt_time = models.DateTimeField(verbose_name='дата и время последней попытки')
    attempt = models.BooleanField(verbose_name='статус попытки')
    response = models.CharField(max_length=100,verbose_name='ответ почтового сервера',**NULLABLE)

    class Meta:
        verbose_name = "лог попыток отправки письма"
        verbose_name_plural = "логи попыток отправки писем"

    def __str__(self):
        return f'{self.attempt_time} - {self.attempt}'










