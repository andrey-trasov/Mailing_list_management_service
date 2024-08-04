import secrets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from myproject.settings import EMAIL_HOST_USER


from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from user.forms import UserRegisterForm
from user.models import User


class UserCreateView(CreateView):
   model = User
   form_class = UserRegisterForm
   success_url = reverse_lazy('user:login')


   def form_valid(self, form):
       user = form.save()   #сохраняем пользователя
       user.is_active = False    #устанавливаем значение "неактивный"
       token = secrets.token_hex(16)    #генерируем токен
       user.token = token    #сохраняем токен в поле token в модели User
       user.save()   #сохраняем изменения в базу
       host = self.request.get_host()   #получаем хост с которого пришел пользователь
       url = f'http://{host}/user/email-confirm/{token}/'   #ссылка которая отправится пользователю
       send_mail(
           subject = 'Подтверждение почты',    #тема письма
           message = f'Перейди по ссылке для подтверждения почты {url}',    #сообщение
           from_email = EMAIL_HOST_USER,    #с какого мейла отправляем
           recipient_list = [user.email]    #список имейлов на которые отправляем
       )
       return super().form_valid(form)   #возвращаем родительский метод, который отправляет данные в форму и сохраняет в базу


def email_verification(request, token):
    user = get_object_or_404(User, token=token)  # получаем пользователя по токену
    user.is_active = True  # меняем статус пользователя на активный
    user.save()  # сохраняем изменения в базу
    return redirect(reverse('user:login'))

