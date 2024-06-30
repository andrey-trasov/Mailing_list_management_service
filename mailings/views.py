from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from mailings.models import Client, Message

#Клиенты
class ClientListView(ListView):
    model = Client

class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'fio', 'comment']
    success_url = reverse_lazy('mailings:client_list')

class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'fio', 'comment']
    success_url = reverse_lazy('mailings:client_list')

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')

class ClientDetailView(DetailView):
    model = Client

#Сообщения
class MessageListView(ListView):
    model = Message

class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    success_url = reverse_lazy('mailings:message_list')

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    success_url = reverse_lazy('mailings:message_list')

class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')

class MessageDetailView(DetailView):
    model = Message


