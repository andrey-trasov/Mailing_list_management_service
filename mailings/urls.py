from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView, NewsletterListView, \
    NewsletterCreateView, NewsletterUpdateView, NewsletterDeleteView, NewsletterDetailView

app_name = MailingsConfig.name
urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>/',ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/',MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('newsletter_list/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletter_create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter_update/<int:pk>/',NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter_delete/<int:pk>/', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter_detail')
]


