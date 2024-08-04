from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField
from user.models import User


class StyleFormMixin:
   """
    Форма для стализации
   """
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for fild_name, fild in self.fields.items():
           if isinstance(fild, BooleanField):
               fild.widget.attrs['class'] = 'form-check-input'
           else:
               fild.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
   """
   Форма для регистрации пользователей с включенными полями email и пароля.
   """
   class Meta:
       model = User
       fields = ['email', 'password1', 'password2']