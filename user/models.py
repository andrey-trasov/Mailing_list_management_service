from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
   username =  None    #обязательные параметры

   email = models.EmailField(unique=True, verbose_name='Email')    #поле для авторизации
   phone = models.CharField(max_length=50, verbose_name='Телефон', help_text='Введите свой телефон', blank=True,
                            null=True)
   token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)

   USERNAME_FIELD = "email"   #обязательные параметры, поле для авторизации
   REQUIRED_FIELDS = []    #обязательные параметры


   class Meta:
       verbose_name = 'пользователь'
       verbose_name_plural = 'пользователи'
       permissions = [
           ("can_view_the_list_of_users_of_the_service", "может просматривать список пользователей сервиса"),
           ("it_can_block_users_of_the_service", "может блокировать пользователей сервиса")
       ]

   def __str__(self):
       return self.email
