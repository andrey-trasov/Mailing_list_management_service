from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailings.forms import ClientForm, MessageForm, NewsletterForm
from mailings.models import Client, Message, Newsletter, Logs

#Клиенты
class ClientListView(ListView):
    model = Client

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user  # получаю авторизованного пользователя
        product.owner = user
        product.save()
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['email', 'fio', 'comment']
    success_url = reverse_lazy('mailings:client_list')

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')

class ClientDetailView(DetailView):
    model = Client

#Сообщения
class MessageListView(ListView):
    model = Message

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    forms = MessageForm
    success_url = reverse_lazy('mailings:message_list')

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['subject', 'body']
    success_url = reverse_lazy('mailings:message_list')

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')

class MessageDetailView(DetailView):
    model = Message

#Рассылка

class NewsletterListView(ListView):
    model = Newsletter

class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    forms = NewsletterForm
    success_url = reverse_lazy('mailings:client_list')

class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    fields = ["name", "start_time", "end_time", "periodicity", "status", "message"]
    success_url = reverse_lazy('mailings:client_list')

class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mailings:client_list')

class NewsletterDetailView(DetailView):
    model = Newsletter


class LogsListView(ListView):
    model = Logs

