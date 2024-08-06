from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from user.apps import UserConfig
from user.views import UserCreateView, email_verification, UserListView, UserUpdateView

app_name = UserConfig.name


urlpatterns = [
   path('', LoginView.as_view(template_name='user/login.html'), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('register/', UserCreateView.as_view(), name='register'),
   path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
   path('user_list/', UserListView.as_view(), name='user_list'),
   path('user_update/<int:pk>/',UserUpdateView.as_view(), name='user_update'),

]
